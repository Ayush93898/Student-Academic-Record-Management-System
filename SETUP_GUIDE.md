# MySQL Setup Guide for Student Management System

## Overview
This application requires a MySQL database server. Since Replit doesn't provide MySQL by default, you have several options:

## Option 1: Run Locally (Recommended)

### For Windows:
1. Download and install [XAMPP](https://www.apachefriends.org/) or [MySQL Installer](https://dev.mysql.com/downloads/installer/)
2. Start MySQL server from XAMPP Control Panel or MySQL Workbench
3. Default credentials:
   - Host: localhost
   - User: root
   - Password: (empty)
   - Port: 3306

### For macOS:
```bash
# Install MySQL using Homebrew
brew install mysql

# Start MySQL server
brew services start mysql

# Secure installation (optional but recommended)
mysql_secure_installation
```

### For Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Fedora/RHEL
sudo dnf install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

## Option 2: Use Remote MySQL Database

If you have access to a remote MySQL database (e.g., AWS RDS, Google Cloud SQL, or any hosting provider):

1. Update `src/database/db_config.py`:
```python
db_config = DatabaseConfig(
    host='your-remote-host.com',    # Your database host
    user='your_username',            # Your database username
    password='your_password',        # Your database password
    database='student_management'    # Database name
)
```

2. Ensure the remote database allows connections from your IP address

## Option 3: Use Docker (Advanced)

If you have Docker installed:

```bash
# Run MySQL in a container
docker run --name mysql-student-mgmt \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=student_management \
  -p 3306:3306 \
  -d mysql:8.0

# Update src/database/db_config.py with password='root'
```

## Verifying MySQL Installation

### Check if MySQL is running:

**Windows (XAMPP):**
- Open XAMPP Control Panel
- Check if MySQL status shows "Running"

**macOS/Linux:**
```bash
# Check MySQL status
sudo systemctl status mysql  # or mysqld

# Test connection
mysql -u root -p
```

### Create Database Manually (Optional):

The application will auto-create the database, but you can do it manually:

```sql
mysql -u root -p

CREATE DATABASE student_management;
USE student_management;

# Run the SQL script
SOURCE src/database/db_init.sql;

# Verify tables were created
SHOW TABLES;
```

## Troubleshooting

### Connection Refused Error:
- **Cause**: MySQL server is not running
- **Solution**: Start MySQL server using appropriate method for your OS

### Access Denied Error:
- **Cause**: Incorrect username or password
- **Solution**: Update credentials in `src/database/db_config.py`

### Can't Connect Error (Port 3306):
- **Cause**: MySQL not listening on port 3306
- **Solution**: Check MySQL configuration file (my.cnf or my.ini)

### Database Doesn't Exist:
- **Cause**: Database not created
- **Solution**: Let the application create it automatically or create manually

## Testing the Application

Once MySQL is set up:

1. Run the application:
```bash
python main.py
```

2. The application will:
   - Connect to MySQL
   - Create database if needed
   - Initialize tables
   - Show login window

3. Login with default credentials:
   - Username: admin
   - Password: admin123

## Quick Setup Checklist

- [ ] MySQL server installed
- [ ] MySQL server running
- [ ] Database credentials configured in `src/database/db_config.py`
- [ ] Required Python packages installed (`mysql-connector-python`, `pillow`)
- [ ] Application starts without connection errors

## Alternative: PostgreSQL Version

If you prefer using PostgreSQL (available on Replit), a separate version can be created using Replit's built-in PostgreSQL database. Contact for modifications.

---

**Note**: This is a learning project designed for educational purposes. MySQL integration teaches database concepts and SQL operations.
