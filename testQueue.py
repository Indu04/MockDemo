'''
Created on Sep 4, 2017

@author: Indu
'''
import unittest
from boto.sqs.message import Message
from mock import patch, Mock

from queue import Queue

def my_local_getQueue(queueName):
    return queueName + "ABCD"

class TestCaseQueue(unittest.TestCase):
 
#     def test_initialize_without_mock(self):
#         """
#         Test initialization
#         """
#         queueName = "TestQueue"
#         queue = Queue("testQueue")
#         self.assertIsNotNone(queue._queue)
  
    @patch.object(Queue, '_get_queue')
    # This is the same as below
    # @patch('queue.Queue._get_queue')
    def test_queue_initialization(self, get_queue_mock):
        """
        patch replaces the class with a mock object and lets you work with the mock instance
    
        * To check that a method called only once:
           `assert_called_once_with`
         * To check the last call: `assert_called_with`
         * To check that a particular call is done among other:
           `assert_any_call`
    
        """
        queueName = "TestQueue"
        queue = Queue(queueName)
        get_queue_mock.assert_called_once_with(queueName)
        print "*********_queue Value : {} \n".format(queue._queue)
        print "*********_get_queue mock return value : {} \n".format(get_queue_mock.return_value)
        self.assertIsNotNone(queue._queue)
        self.assertEqual(queue._queue, get_queue_mock.return_value)
#  
    # Mock the imported module
    @patch('queue.connect_to_region')
    def test_get_queue(self, connect_to_region_mock):
        """
        mocking object, should be done were it will be used.
        Here connect_to_region comes from boto but it is imported and
        used in queue
         
        Here connect_to_region returns a connection object from which
        we call the get_queue method. That's why we need the
        connect_to_region_mock to return the sqs_connection_mock.
         
        Two way to know if a method (i.e. a mock) have been called:
         * my_mock.called: returns a boolean regardless the number
           of call
         * my_mock.call_count: returns the actual number of call
         
        """
        queueName = "TestQueue"
        mockQueueObjName = "MockQueueObj"
          
        connection_obj__mock = Mock()
        print "Connection Obj Mock ", connection_obj__mock
        print "Connect_to_region_function Mock", connect_to_region_mock
        connection_obj__mock.get_queue.return_value = mockQueueObjName
        connect_to_region_mock.return_value = connection_obj__mock
     
        queue = Queue(queueName)
        self.assertTrue(connect_to_region_mock.called)
        assert queue._queue == mockQueueObjName
        connection_obj__mock.get_queue.assert_called_once_with(queueName)
#     
#     @patch.object(Queue, '_get_queue')
#     def test_is_empty(self, get_queue_mock):
#         """
#         If you understand the previous examples this test is
#         straightforward.
#         
#         We create a mocked queue object that will respond to count
#         with our value.
#         """
#         queueName = "TestQueue"
#         
#         queue_mock = Mock()
#         queue_mock.count.return_value = 10
#         get_queue_mock.return_value = queue_mock
#         queue = Queue(queueName)
#         self.assertFalse(queue.is_empty)
#         
#         queue_mock.count.return_value = 0
#         get_queue_mock.return_value = queue_mock
#         queue = Queue(queueName)
#         self.assertTrue(queue.is_empty)
#           
    @patch('queue.Message')
    # Notice the argument order
    @patch.object(Queue, '_get_queue')
    def test_push_multiple_messages(self,
                                    get_queue_mock,
                                    message_mock):
        """
        Notice the decoration and parameter order: the first
        parameter is the closest to the function name (thing how
        decorator are called).
            
        write called as many times as number of messages
        """
        queueName = "TestQueue"
        message1 = "TestMessage1"
        message2 = "TestMessage2"
           
        queue_mock = Mock()
        get_queue_mock.return_value = queue_mock
           
        envelope_mock = Mock()
        message_mock.return_value = envelope_mock
            
        queue = Queue(queueName)
        queue.push(message1, message2)
     
        self.assertEqual(queue_mock.write.call_count, 2)
        envelope_mock.set_body.assert_any_call(message1)
        envelope_mock.set_body.assert_called_with(message2)
#   
    @patch.object(Queue, '_get_queue', side_effect=my_local_getQueue)
    def test_queue_customQueue(self, get_queue_mock):
        """
        side_effect replaces entire function with other function
        """
        queueName = "TestQueue"
        queue = Queue(queueName)
        get_queue_mock.assert_called_once_with(queueName)
        print "*********_queue Value : ", queue._queue
        self.assertEqual(queue._queue, 'TestQueueABCD')

