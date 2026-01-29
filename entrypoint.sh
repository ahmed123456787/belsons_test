#!/bin/bash

################################################################################
# Belsons News - Project Entrypoint Script
# 
# This script automates the setup and startup of the entire project.
# It handles Docker Compose initialization, database migrations, and service startup.
#
# Usage: ./entrypoint.sh [command]
# Commands:
#   start          - Build and start all services (default)
#   stop           - Stop all running services
#   restart        - Restart all services
#   logs           - View logs from all services
#   clean          - Remove all containers and volumes
#   help           - Show this help message
################################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

################################################################################
# Prerequisite Checks
################################################################################

check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check for Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker is installed ($(docker --version))"
    
    # Check for Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose is installed ($(docker-compose --version))"
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    print_success "Docker daemon is running"
}

################################################################################
# Environment Setup
################################################################################

setup_environment() {
    print_header "Setting Up Environment"
    
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        print_info "Creating .env file with default values..."
        cat > "$PROJECT_ROOT/.env" << EOF
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -base64 32)

# PostgreSQL Database
POSTGRES_DB=news_db
POSTGRES_USER=news_user
POSTGRES_PASSWORD=secure_password_123
POSTGRES_HOST=postgres

# NewsAPI
NEWSAPI_KEY=your_newsapi_key_here

# Redis
REDIS_URL=redis://redis:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EOF
        print_success ".env file created"
        print_info "Please update NEWSAPI_KEY in .env file with your actual API key from https://newsapi.org/"
    else
        print_success ".env file already exists"
    fi
}

################################################################################
# Docker Operations
################################################################################

docker_build() {
    print_header "Building Docker Images"
    
    cd "$PROJECT_ROOT"
    if docker-compose build; then
        print_success "Docker images built successfully"
    else
        print_error "Failed to build Docker images"
        exit 1
    fi
}

docker_start() {
    print_header "Starting Services"
    
    cd "$PROJECT_ROOT"
    if docker-compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

docker_stop() {
    print_header "Stopping Services"
    
    cd "$PROJECT_ROOT"
    if docker-compose down; then
        print_success "Services stopped successfully"
    else
        print_error "Failed to stop services"
        exit 1
    fi
}

docker_restart() {
    print_header "Restarting Services"
    
    docker_stop
    sleep 2
    docker_start
    print_success "Services restarted successfully"
}

docker_logs() {
    print_header "Displaying Logs"
    
    cd "$PROJECT_ROOT"
    docker-compose logs -f
}

docker_clean() {
    print_header "Cleaning Up Docker Resources"
    
    print_info "This will remove containers, volumes, and networks"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$PROJECT_ROOT"
        docker-compose down -v
        print_success "Docker resources cleaned up"
    else
        print_info "Cleanup cancelled"
    fi
}

################################################################################
# Database Operations
################################################################################

wait_for_database() {
    print_header "Waiting for Database to be Ready"
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose exec -T postgres pg_isready -U news_user > /dev/null 2>&1; then
            print_success "Database is ready"
            return 0
        fi
        
        print_info "Waiting for database... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    print_error "Database did not become ready in time"
    return 1
}

run_migrations() {
    print_header "Running Database Migrations"
    
    cd "$BACKEND_DIR"
    if docker-compose -f "$PROJECT_ROOT/docker-compose.yaml" exec -T web python manage.py migrate; then
        print_success "Database migrations completed"
    else
        print_error "Failed to run migrations"
        return 1
    fi
}

create_superuser() {
    print_header "Django Superuser Setup"
    
    print_info "Creating superuser (admin/admin)..."
    cd "$BACKEND_DIR"
    
    # Try to create superuser (will skip if already exists)
    docker-compose -f "$PROJECT_ROOT/docker-compose.yaml" exec -T web python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser created: admin/admin")
else:
    print("Superuser already exists")
EOF
    
    print_success "Superuser setup completed"
}

################################################################################
# Display Information
################################################################################

display_access_info() {
    print_header "Application is Ready!"
    
    echo -e "${GREEN}Access the application at:${NC}\n"
    echo -e "  ${BLUE}Frontend:${NC}         http://localhost:4200"
    echo -e "  ${BLUE}Backend API:${NC}      http://localhost:8000"
    echo -e "  ${BLUE}API Documentation:${NC} http://localhost:8000/apis/v1/"
    echo -e "  ${BLUE}Django Admin:${NC}     http://localhost:8000/admin/\n"
    
    echo -e "${GREEN}Default Credentials:${NC}\n"
    echo -e "  ${BLUE}Username:${NC} admin"
    echo -e "  ${BLUE}Password:${NC} admin\n"
    
    echo -e "${YELLOW}Important:${NC}"
    echo -e "  • Update NEWSAPI_KEY in .env file before fetching news"
    echo -e "  • Check logs with: docker-compose logs -f"
    echo -e "  • Stop services with: docker-compose down\n"
}

################################################################################
# Main Execution
################################################################################

main() {
    local command="${1:-start}"
    
    case "$command" in
        start)
            print_header "🚀 Starting Belsons News Application"
            check_prerequisites
            setup_environment
            docker_build
            docker_start
            
            # Wait for services to be ready
            sleep 5
            
            if wait_for_database; then
                run_migrations
                create_superuser
                display_access_info
            else
                print_error "Failed to start application due to database connection issues"
                exit 1
            fi
            ;;
            
        stop)
            docker_stop
            ;;
            
        restart)
            docker_restart
            display_access_info
            ;;
            
        logs)
            docker_logs
            ;;
            
        clean)
            docker_clean
            ;;
            
        help)
            echo "Belsons News - Project Entrypoint Script"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  start              Build and start all services (default)"
            echo "  stop               Stop all running services"
            echo "  restart            Restart all services"
            echo "  logs               View logs from all services"
            echo "  clean              Remove all containers and volumes"
            echo "  help               Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 start       # Start the application"
            echo "  $0 logs        # View real-time logs"
            echo "  $0 stop        # Stop all services"
            ;;
            
        *)
            print_error "Unknown command: $command"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
