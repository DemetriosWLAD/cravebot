#!/usr/bin/env python3
"""
Deployment Validation Script for CraveBreaker Bot
Tests all deployment components and endpoints
"""

import asyncio
import os
import sys
import json
import time
import subprocess
from flask import Flask
import aiosqlite
import httpx

class DeploymentValidator:
    def __init__(self):
        self.results = {
            "timestamp": time.time(),
            "tests": {},
            "summary": {"passed": 0, "failed": 0, "total": 0}
        }
        
    def test_result(self, test_name, passed, message=""):
        """Record test result"""
        self.results["tests"][test_name] = {
            "passed": passed,
            "message": message,
            "timestamp": time.time()
        }
        if passed:
            self.results["summary"]["passed"] += 1
            print(f"✅ {test_name}: {message}")
        else:
            self.results["summary"]["failed"] += 1
            print(f"❌ {test_name}: {message}")
        self.results["summary"]["total"] += 1
    
    def test_environment_variables(self):
        """Test required environment variables"""
        print("\n🔍 Testing Environment Variables...")
        
        # Test TELEGRAM_BOT_TOKEN
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token and len(token) > 10:
            self.test_result("env_telegram_token", True, "TELEGRAM_BOT_TOKEN configured")
        else:
            self.test_result("env_telegram_token", False, "TELEGRAM_BOT_TOKEN missing or invalid")
            
        # Test SESSION_SECRET
        session_secret = os.getenv('SESSION_SECRET')
        if session_secret:
            self.test_result("env_session_secret", True, "SESSION_SECRET configured")
        else:
            self.test_result("env_session_secret", False, "SESSION_SECRET missing")
            
        # Test PORT
        port = os.getenv('PORT', '5000')
        try:
            port_int = int(port)
            if 1000 <= port_int <= 65535:
                self.test_result("env_port", True, f"PORT configured: {port}")
            else:
                self.test_result("env_port", False, f"PORT invalid: {port}")
        except ValueError:
            self.test_result("env_port", False, f"PORT not numeric: {port}")
    
    def test_file_structure(self):
        """Test critical files exist"""
        print("\n📁 Testing File Structure...")
        
        critical_files = [
            "main.py",
            "simple_bot.py", 
            "wsgi.py",
            "replit_deploy.toml",
            "pyproject.toml",
            "Procfile",
            "Dockerfile",
            "gunicorn.conf.py"
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                self.test_result(f"file_{file_path}", True, f"{file_path} exists")
            else:
                self.test_result(f"file_{file_path}", False, f"{file_path} missing")
    
    def test_python_imports(self):
        """Test critical Python imports"""
        print("\n🐍 Testing Python Imports...")
        
        imports_to_test = [
            ("flask", "Flask"),
            ("aiosqlite", "aiosqlite"),
            ("httpx", "httpx"),
            ("simple_bot", "SimpleCraveBreakerBot"),
        ]
        
        for module, component in imports_to_test:
            try:
                __import__(module)
                self.test_result(f"import_{module}", True, f"{module} imports successfully")
            except ImportError as e:
                self.test_result(f"import_{module}", False, f"{module} import failed: {e}")
    
    async def test_database_initialization(self):
        """Test database initialization"""
        print("\n🗄️ Testing Database...")
        
        try:
            from simple_bot import SimpleCraveBreakerBot
            bot = SimpleCraveBreakerBot()
            await bot.init_db()
            
            # Test database connection
            async with aiosqlite.connect(bot.db_path) as db:
                cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = await cursor.fetchall()
                table_names = [table[0] for table in tables]
                
                required_tables = ["users", "help_requests", "interventions", "user_progress"]
                missing_tables = [table for table in required_tables if table not in table_names]
                
                if not missing_tables:
                    self.test_result("database_init", True, f"Database initialized with {len(table_names)} tables")
                else:
                    self.test_result("database_init", False, f"Missing tables: {missing_tables}")
                    
        except Exception as e:
            self.test_result("database_init", False, f"Database initialization failed: {e}")
    
    def test_flask_app_creation(self):
        """Test Flask app can be created"""
        print("\n🌐 Testing Flask App...")
        
        try:
            from main import app
            if app and isinstance(app, Flask):
                self.test_result("flask_app", True, "Flask app created successfully")
                
                # Test routes exist
                routes = [rule.rule for rule in app.url_map.iter_rules()]
                expected_routes = ["/", "/health", "/status", "/restart"]
                
                missing_routes = [route for route in expected_routes if route not in routes]
                if not missing_routes:
                    self.test_result("flask_routes", True, f"All routes available: {routes}")
                else:
                    self.test_result("flask_routes", False, f"Missing routes: {missing_routes}")
            else:
                self.test_result("flask_app", False, "Flask app not created properly")
                
        except Exception as e:
            self.test_result("flask_app", False, f"Flask app creation failed: {e}")
    
    def test_deployment_configs(self):
        """Test deployment configuration files"""
        print("\n⚙️ Testing Deployment Configs...")
        
        # Test replit_deploy.toml
        try:
            import toml
            with open("replit_deploy.toml", "r") as f:
                config = toml.load(f)
                
            if config.get("deployment", {}).get("run") == "python main.py":
                self.test_result("deploy_config_run", True, "Replit deploy run command correct")
            else:
                self.test_result("deploy_config_run", False, "Replit deploy run command incorrect")
                
            if config.get("deployment", {}).get("health", {}).get("path") == "/health":
                self.test_result("deploy_config_health", True, "Health check path configured")
            else:
                self.test_result("deploy_config_health", False, "Health check path not configured")
                
        except Exception as e:
            self.test_result("deploy_config", False, f"Deployment config test failed: {e}")
            
        # Test Procfile
        try:
            with open("Procfile", "r") as f:
                procfile_content = f.read()
            
            if "python main.py" in procfile_content:
                self.test_result("procfile", True, "Procfile configured correctly")
            else:
                self.test_result("procfile", False, "Procfile configuration incorrect")
                
        except Exception as e:
            self.test_result("procfile", False, f"Procfile test failed: {e}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🎯 DEPLOYMENT VALIDATION SUMMARY")
        print("="*60)
        
        summary = self.results["summary"]
        total = summary["total"]
        passed = summary["passed"]
        failed = summary["failed"]
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
        
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for test_name, result in self.results["tests"].items():
                if not result["passed"]:
                    print(f"  • {test_name}: {result['message']}")
        
        print("\n" + "="*60)
        
        # Save results to file
        with open("deployment_validation_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        return failed == 0

async def main():
    """Run all deployment validation tests"""
    print("🚀 CraveBreaker Deployment Validation")
    print("="*50)
    
    validator = DeploymentValidator()
    
    # Run all tests
    validator.test_environment_variables()
    validator.test_file_structure()
    validator.test_python_imports()
    await validator.test_database_initialization()
    validator.test_flask_app_creation()
    validator.test_deployment_configs()
    
    # Print summary
    success = validator.print_summary()
    
    if success:
        print("🎉 All deployment checks passed! Ready for deployment.")
        return 0
    else:
        print("⚠️ Some deployment checks failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)