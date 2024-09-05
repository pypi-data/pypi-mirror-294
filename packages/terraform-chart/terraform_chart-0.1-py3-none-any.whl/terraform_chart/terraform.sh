#!/bin/bash

# Your GitHub credentials
GITHUB_USER="terra-gcp"
GITHUB_TOKEN="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"

# Function to create directory structure
create_directory_structure() {
    local module_name=$1

    # Creating the main directory
    mkdir -p ./"$module_name"/{calling/{build-file,input-file,log-file/{apply,destroy},output-file,plan-file,template},module/terraform-google-$module_name}

    # Creating the files
    touch ./"$module_name"/calling/{$module_name-apply.sh,$module_name-destroy.sh}
    touch ./"$module_name"/calling/build-file/{cloudbuild-tf-apply.yaml,cloudbuild-tf-destroy.yaml,cloudbuild-tf-plan.yaml}
    touch ./"$module_name"/calling/input-file/{default.tfvars,variable.tfvars}
    touch ./"$module_name"/calling/log-file/apply/readme.txt
    touch ./"$module_name"/calling/log-file/destroy/readme.txt
    touch ./"$module_name"/calling/output-file/readme.txt
    touch ./"$module_name"/calling/plan-file/readme.txt
    touch ./"$module_name"/calling/template/{backend.tf,$module_name.tf,locals.tf,outputs.tf,provider.tf,variables.tf}
    touch ./"$module_name"/module/{Readme.md,terraform-google-$module_name/{main.tf,outputs.tf,variables.tf,versions.tf}}
    touch ./"$module_name"/module/Readme.md

    echo -e ""
    echo "Terraform module '$module_name' structure created successfully."
    echo -e ""
}

# Function to check if a module folder exists in the GitHub repository
check_and_clone_repo() {
    local module_name=$1
    local repo_url="https://github.com/Terra-GCP/advanced-iaac-modules-gcp"
    local check_url="https://api.github.com/repos/Terra-GCP/advanced-iaac-modules-gcp/contents/$module_name"

    # Check if module directory exists in the GitHub repository
    http_response=$(curl --write-out "%{http_code}" --silent --output /dev/null -u "$GITHUB_USER:$GITHUB_TOKEN" "$check_url")

    if [ "$http_response" -eq 200 ]; then
        git clone https://$GITHUB_USER:$GITHUB_TOKEN@github.com/Terra-GCP/advanced-iaac-modules-gcp.git temp_repo > /dev/null 2>&1
        cp -r temp_repo/"$module_name" ./
        rm -rf temp_repo
        echo -e ""
        echo "Terraform module '$module_name' structure created successfully."
        echo -e ""
    else
        create_directory_structure "$module_name"
    fi
}

# Function to pull a module from the GitHub repository
pull_module() {
    local module_name=$1

    echo -e ""
    git clone https://$GITHUB_USER:$GITHUB_TOKEN@github.com/Terra-GCP/advanced-iaac-modules-gcp.git --depth=1 --filter=blob:none --sparse temp_repo > /dev/null 2>&1
    cd temp_repo

    # Check if the module exists in the repository
    git sparse-checkout set "$module_name" > /dev/null 2>&1
    if [ ! -d "$module_name" ]; then
        echo "Module '$module_name' does not exist in the repository."
        echo -e ""
        cd ..
        rm -rf temp_repo
        return 1
    fi

    cd ..
    cp -r temp_repo/"$module_name" ./
    rm -rf temp_repo
    echo "Module '$module_name' pulled successfully."
    echo -e ""
}

# Function to list all modules in the GitHub repository
list_modules() {
    local repo_url="https://api.github.com/repos/Terra-GCP/advanced-iaac-modules-gcp/contents"

    # Fetch the list of directories in the repository
    echo -e ""
    curl -s -u "$GITHUB_USER:$GITHUB_TOKEN" "$repo_url" | jq -r '.[] | select(.type == "dir") | .name'
    echo -e ""
}

# Function to delete a module locally
delete_module() {
    local module_name=$1

    if [ -d "$module_name" ]; then
        rm -rf "$module_name"
        echo -e ""
        echo "Module '$module_name' deleted successfully."
        echo -e ""
    else
        echo -e ""
        echo "Module '$module_name' does not exist."
        echo -e ""
    fi
}

# Check if module name is provided
if [ -z "$1" ]; then
    echo -e ""
    echo "Usage: terraform chart <command> <module_name>"
    echo "Commands:"
    echo "  create <module_name>   - Create a module"
    echo "  list                   - List all modules in the repository"
    echo "  delete <module_name>   - Delete a module"
    echo "  pull <module_name>     - Pull a module from the repository"
    echo -e ""
    exit 1
fi

# Handle the command provided
case "$1" in
    create)
        if [ -z "$2" ]; then
            echo -e ""
            echo "Please provide the module name."
            echo -e ""
            exit 1
        fi
        check_and_clone_repo "$2"
        ;;
    list)
        list_modules
        ;;
    delete)
        if [ -z "$2" ]; then
            echo -e ""
            echo "Please provide the module name."
            echo -e ""
            exit 1
        fi
        delete_module "$2"
        ;;
    pull)
        if [ -z "$2" ]; then
            echo -e ""
            echo "Please provide the module name."
            echo -e ""
            exit 1
        fi
        pull_module "$2"
        ;;
    *)
        echo "Invalid command. Use 'create', 'list', 'delete', or 'pull'."
        exit 1
        ;;
esac