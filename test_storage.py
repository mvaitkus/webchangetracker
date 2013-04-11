import unittest
import os
from storage import Storage

class StorageTest(unittest.TestCase):
    
    DB_FILE_NAME = 'test.db'
    
    TEST_SITE1 = 'test1'
    
    TEST_SITE2 = 'test2'
    
    DATA = {'key' : 100}
    
    MORE_DATA = {'newKey' : 50, 'key': 200}
    
    def setUp(self):
        if os.path.exists(self.DB_FILE_NAME):
            os.remove(self.DB_FILE_NAME) # should I rename instead?
    
    def test_creates_database_file_after_construction(self):
        storage = Storage(self.DB_FILE_NAME)
        self.assertTrue(os.path.exists(self.DB_FILE_NAME),"Should create local file with passed db name")
        
    def test_select_doesnt_fail_for_no_data(self):
        storage = Storage(self.DB_FILE_NAME)
        self.assertTrue(storage.get_items(self.TEST_SITE1) == {}, "Should return no items if nothing was inserted")
        
    def test_select_returns_inserted_data(self):
        storage = Storage(self.DB_FILE_NAME)
        storage.insert_items(self.TEST_SITE1, self.DATA)
        self.assertTrue(storage.get_items(self.TEST_SITE1) == self.DATA, "Should return inserted items")
        
    def test_select_doesnt_return_data_for_other_site(self):
        storage = Storage(self.DB_FILE_NAME)
        storage.insert_items(self.TEST_SITE1, self.DATA)
        self.assertTrue(storage.get_items(self.TEST_SITE2) == {}, "Should have no data for site2 as it wasn't inserted")
        
    def test_select_retrieves_updated_data(self):
        storage = Storage(self.DB_FILE_NAME)
        storage.insert_items(self.TEST_SITE1, self.MORE_DATA)
        storage.change_items(self.TEST_SITE1, self.DATA)
        self.assertTrue(storage.get_items(self.TEST_SITE1)['key'] == 100, "Should have updated value for key")
        
    def test_remove_deletes_items_by_key(self):
        storage = Storage(self.DB_FILE_NAME)
        storage.insert_items(self.TEST_SITE1, self.MORE_DATA)
        storage.remove_items(self.TEST_SITE1, self.DATA)
        self.assertTrue('key' not in storage.get_items(self.TEST_SITE1), "Should not contain removed items")
        self.assertTrue('newKey' in storage.get_items(self.TEST_SITE1), "Should contain key that was not passed for removal")
        
    def tearDown(self):
        os.remove(self.DB_FILE_NAME)
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StorageTest('test_creates_database_file_after_construction'))
    suite.addTest(StorageTest('test_select_doesnt_fail_for_no_data'))
    suite.addTest(StorageTest('test_select_returns_inserted_data'))
    suite.addTest(StorageTest('test_select_doesnt_return_data_for_other_site'))
    suite.addTest(StorageTest('test_select_retrieves_updated_data'))
    suite.addTest(StorageTest('test_remove_deletes_items_by_key'))
    return suite

if __name__ == '__main__':
    unittest.main()
