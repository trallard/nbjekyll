""" Base TestCase for testing nb_git"""
import gc
import os
import shutil
import unittest
import tempfile

class NoRepoTestCase(unittest.TestCase):

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self.repo = None

    def tearDown(self):
        del self.repo
        gc.collect()
        rmtree(self._temp_dir)

    def assertRaisesAssign(self, exc_class, instance, name, value):
        try:
            setattr(instance, name, value)
        except:
            self.assertEqual(exc_class, sys.exc_info()[0])

    def assertAll(self, func, entries):
        return self.assertTrue(all(func(x) for x in entries))

    def assertAny(self, func, entries):
        return self.assertTrue(any(func(x) for x in entries))

    def assertRaisesWithArg(self, exc_class, arg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exc_class as exc_value:
            self.assertEqual((arg,), exc_value.args)
        else:
            self.fail('%s(%r) not raised' % (exc_class.__name__, arg))

    def assertEqualSignature(self, a, b):
        # XXX Remove this once equality test is supported by Signature
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.email, b.email)
        self.assertEqual(a.time, b.time)
        self.assertEqual(a.offset, b.offset)


def rmtree(path):
    """In Windows a read-only file cannot be removed, and shutil.rmtree fails.
    So we implement our own version of rmtree to address this issue.
    """
    if os.path.exists(path):
        onerror = lambda func, path, e: force_rm_handle(func, path, e)
        shutil.rmtree(path, onerror=onerror)

