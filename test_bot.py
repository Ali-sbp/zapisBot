#!/usr/bin/env python3
"""
Test script for University Course Registration Bot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import QueueManager, UniversityRegistrationBot
import json
import tempfile

def test_queue_manager():
    """Test QueueManager functionality"""
    print("🧪 Testing QueueManager...")
    
    # Create temporary data file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    # Initialize queue manager with test file
    qm = QueueManager()
    qm.data_file = temp_file
    qm.registration_open = True
    
    # Test adding users to queue
    success1, msg1 = qm.add_to_queue('math101', 12345, 'testuser1', 'Test User One')
    assert success1, f"Failed to add user: {msg1}"
    print(f"✅ Added user 1: {msg1}")
    
    success2, msg2 = qm.add_to_queue('math101', 67890, 'testuser2', 'Test User Two')
    assert success2, f"Failed to add user: {msg2}"
    print(f"✅ Added user 2: {msg2}")
    
    # Test duplicate prevention
    success3, msg3 = qm.add_to_queue('math101', 12345, 'testuser1', 'Test User One')
    assert not success3, "Should have prevented duplicate registration"
    print(f"✅ Duplicate prevention: {msg3}")
    
    # Test queue status
    status = qm.get_queue_status('math101')
    print(f"✅ Queue status: {status}")
    
    # Test closed registration
    qm.close_registration()
    success4, msg4 = qm.add_to_queue('phys201', 11111, 'testuser3', 'Test User Three')
    assert not success4, "Should have prevented registration when closed"
    print(f"✅ Closed registration: {msg4}")
    
    # Clean up
    os.unlink(temp_file)
    print("🎉 QueueManager tests passed!")

def test_bot_configuration():
    """Test bot configuration"""
    print("🧪 Testing bot configuration...")
    
    # Check if required environment variables are set
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    assert token, "TELEGRAM_BOT_TOKEN not found in environment"
    assert len(token) > 10, "Bot token seems invalid"
    print("✅ Bot token found and valid format")
    
    # Check configuration file
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    assert 'courses' in config, "Courses not found in config"
    assert len(config['courses']) > 0, "No courses configured"
    print(f"✅ Found {len(config['courses'])} courses in configuration")
    
    print("🎉 Configuration tests passed!")

def test_data_persistence():
    """Test data persistence"""
    print("🧪 Testing data persistence...")
    
    # Create temporary data file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    # Create first queue manager and add data
    qm1 = QueueManager()
    qm1.data_file = temp_file
    qm1.registration_open = True
    qm1.add_to_queue('cs200', 99999, 'testuser', 'Persistent Test User')
    qm1.save_data()
    
    # Create second queue manager and load data
    qm2 = QueueManager()
    qm2.data_file = temp_file
    qm2.load_data()
    
    # Verify data was loaded
    assert len(qm2.queues['cs200']) == 1, "Data was not persisted correctly"
    assert qm2.queues['cs200'][0]['full_name'] == 'Persistent Test User', "User data not correct"
    assert qm2.registration_open == True, "Registration status not persisted"
    
    print("✅ Data persistence working correctly")
    
    # Clean up
    os.unlink(temp_file)
    print("🎉 Persistence tests passed!")

def main():
    """Run all tests"""
    print("🚀 Starting University Registration Bot Tests\n")
    
    try:
        test_queue_manager()
        print()
        test_bot_configuration()
        print()
        test_data_persistence()
        print()
        print("🎉 All tests passed! Bot is ready to use.")
        print("\n📋 Next steps:")
        print("1. Run 'python main.py' to start the bot")
        print("2. Add the bot to your university group")
        print("3. Test with /start command")
        print("4. Use /admin_open to manually open registration for testing")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()