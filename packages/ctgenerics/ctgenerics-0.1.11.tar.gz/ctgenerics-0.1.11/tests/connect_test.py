from unittest import TestCase,main
from unittest.mock import patch, MagicMock
from ctgenerics import connect
class TestConnection(TestCase):
    
    def test_init_with_explicit_config_path(self):
        """Test initialization with an explicitly provided config path."""
        with patch('os.path.exists', return_value=True), \
             patch('ctgenerics.connect.load_dbconfig', return_value=MagicMock(user='user', password='pass', host='host', port=5439, dbname='dbname')), \
             patch('ctgenerics.connect.create_engine') as mock_create_engine:
            connect.Redshift('source', config_path='/explicit/path/to/config.yaml')
            mock_create_engine.assert_called_once()

    def test_init_with_env_variable(self):
        """Test initialization with configuration path provided via environment variable."""
        with patch.dict('os.environ', {'CTGENERICS_CONFIG': '/env/path/to/config.yaml'}), \
             patch('os.path.exists', return_value=True), \
             patch('ctgenerics.connect.load_dbconfig', return_value=MagicMock(user='user', password='pass', host='host', port=5439, dbname='dbname')), \
             patch('ctgenerics.connect.create_engine') as mock_create_engine:
            connect.Redshift('source')
            mock_create_engine.assert_called_once()

    def test_init_with_default_config_path(self):
        """Test initialization using the default configuration path when no other is provided."""
        with patch('os.path.exists', side_effect=lambda path: path == 'config.yaml'), \
             patch('ctgenerics.connect.load_dbconfig', return_value=MagicMock(user='user', password='pass', host='host', port=5439, dbname='dbname')), \
             patch('ctgenerics.connect.create_engine') as mock_create_engine:
            connect.Redshift('source')
            mock_create_engine.assert_called_once()       

    def test_DBConfig_values(self):
        db_config = connect.load_dbconfig('tests/config.yaml','test-db')
        self.assertEqual(db_config.host,'test.dev.redshift.amazonaws.com')
        self.assertEqual(db_config.port,5432)
        self.assertEqual(db_config.dbname,'test-dbname')
        self.assertEqual(db_config.user,'test-user')
        self.assertEqual(db_config.password,'test-password')
        self.assertEqual(db_config.default_schema,'test-schema')

    def test_missing_optionals(self):
        credentials={
            'host':'test.dev.redshift.amazonaws.com',
            'port':5432,
            'dbname':'test-dbname',
            'user':'test-user',
            'password':'test-password'
        }
        db_confg = connect.DBConfig(**credentials)
        self.assertIsInstance(db_confg,connect.DBConfig)
        self.assertIsNone(db_confg.default_schema)
       
    def test_missing_source(self):
        with self.assertRaises(KeyError):
            connect.load_dbconfig('tests/config.yaml','missing-source')

    def test_missing_config(self):
        with self.assertRaises(connect.MissingConfigError):
            connect.connect.Redshift()


  


if __name__ == '__main__':
    main()