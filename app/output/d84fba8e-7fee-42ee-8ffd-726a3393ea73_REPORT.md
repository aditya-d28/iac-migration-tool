# Migration Report: <br>
Resources found in the terraform repository: <br>
 | Resource | Module |
 |-------|-------|
 | azurerm_key_vault_key | ./modules/azurerm_key_vault_key |
 | azurerm_role_definition | ./modules/azurerm_role_definition |
 | azurerm_user_assigned_managed_identity | ./modules/azurerm_user_assigned_managed_identity |
 | azurerm_role_definition | ./modules/azurerm_role_definition |
 | azurerm_postgresql_db_server | ./modules/azurerm_postgresql_db_server |
 | azurerm_postgresql_db_server | ./modules/azurerm_postgresql_db_server |
 | azurerm_redis_cache | ./modules/azurerm_redis_cache |
 | azurerm_storage_container | ./modules/azurerm_storage_container |
## azurerm_key_vault_key ```(./modules/azurerm_key_vault_key)``` <br>
### List of relevant modules:<br>
 - Module: simple_example<br>
   Path: terraform-google-kms/examples/simple_example<br>
 - Module: autokey<br>
   Path: terraform-google-kms/modules/autokey<br>
 <br>
 **Remarks:** The Azure Key Vault Key can be mapped to Google Cloud KMS. The simple_example provides basic key management functionality, while the autokey module offers automatic key rotation capabilities similar to the Azure implementation. Note that some Azure-specific features like curve types may need to be adjusted for GCP compatibility.<br>
<br>
### Module Mapping:<br>
 - Module: simple_example<br>
   Path: terraform-google-kms/examples/simple_example<br>
 <br>
 **Remarks:** The source Azure Key Vault Key module can be mapped to GCP KMS simple_example, which provides similar key management functionality. While not all features have direct equivalents (like curve types specific to Azure), the core functionality of key creation, management, and basic rotation can be implemented. The autokey module was not included as it focuses on automated key management at a folder level, which is a different use case than the source module's single key management.<br>
<br>
## azurerm_role_definition ```(./modules/azurerm_role_definition)``` <br>
### List of relevant modules:<br>
 - Module: custom_role_project<br>
   Path: terraform-google-iam/examples/custom_role_project<br>
 - Module: member_iam<br>
   Path: terraform-google-iam/examples/member_iam<br>
 - Module: custom_role_iam<br>
   Path: terraform-google-iam/modules/custom_role_iam<br>
 <br>
 **Remarks:** The Azure role definition can be migrated using a combination of custom role creation and member IAM binding in GCP. The custom_role_project example and module handle role definition creation, while member_iam handles role assignment. The scope in GCP is project-level instead of resource group level.<br>
<br>
### Module Mapping:<br>
 - Module: custom_role_iam<br>
   Path: terraform-google-iam/modules/custom_role_iam<br>
 <br>
 **Remarks:** The source Azure module creates and assigns custom role definitions, which maps directly to GCP's custom_role_iam module. This module provides similar functionality for creating custom IAM roles with specific permissions and assigning them to principals. The GCP module supports both organization and project-level roles, handles permission management, and includes member assignment capabilities, making it a suitable equivalent for the Azure implementation.<br>
<br>
## azurerm_user_assigned_managed_identity ```(./modules/azurerm_user_assigned_managed_identity)``` <br>
### List of relevant modules:<br>
 - Module: service_accounts<br>
   Path: terraform-google-service-accounts/modules/simple-sa<br>
 - Module: iam_member<br>
   Path: terraform-google-iam/modules/member_iam<br>
 - Module: custom_role<br>
   Path: terraform-google-iam/modules/custom_role_iam<br>
 <br>
 **Remarks:** To replicate Azure's User Assigned Managed Identity functionality in GCP, you'll need a combination of service accounts (equivalent to managed identities) and IAM modules. The simple-sa module creates the service account, member_iam handles role assignments, and custom_role_iam manages custom role definitions and assignments.<br>
<br>
### Module Mapping:<br>
 - Module: service_accounts<br>
   Path: terraform-google-service-accounts/modules/simple-sa<br>
 - Module: iam_member<br>
   Path: terraform-google-iam/modules/member_iam<br>
 - Module: custom_role<br>
   Path: terraform-google-iam/modules/custom_role_iam<br>
 <br>
 **Remarks:** The mapping requires three modules to replicate the Azure User Assigned Identity functionality in GCP: service_accounts for creating the identity, iam_member for role assignments, and custom_role for custom role definitions. This combination provides equivalent functionality for identity creation and role management in GCP.<br>
<br>
## azurerm_role_definition ```(./modules/azurerm_role_definition)``` <br>
### List of relevant modules:<br>
 - Module: custom_role_project<br>
   Path: terraform-google-iam/examples/custom_role_project<br>
 - Module: member_iam<br>
   Path: terraform-google-iam/examples/member_iam<br>
 - Module: custom_role_iam<br>
   Path: terraform-google-iam/modules/custom_role_iam<br>
 <br>
 **Remarks:** The Azure role definition can be mapped using a combination of GCP custom roles and IAM bindings. The custom_role_project example and module handle role creation, while the member_iam example handles role assignment. Both components are needed to replicate the full functionality of the Azure role definition and assignment resources.<br>
<br>
### Module Mapping:<br>
 - Module: custom_role_iam<br>
   Path: terraform-google-iam/modules/custom_role_iam<br>
 <br>
 **Remarks:** The source Azure module creates and assigns custom role definitions, which directly maps to GCP's custom_role_iam module functionality. This module supports both role creation with specific permissions and role assignment to principals, matching the core functionality of the source module. The GCP module handles both organization and project-level roles, providing equivalent capability to Azure's scope-based role definitions.<br>
<br>
## azurerm_postgresql_db_server ```(./modules/azurerm_postgresql_db_server)``` <br>
### List of relevant modules:<br>
 - Module: postgresql<br>
   Path: terraform-google-sql-db/modules/postgresql<br>
 - Module: postgresql-public-iam<br>
   Path: terraform-google-sql-db/examples/postgresql-public-iam<br>
 - Module: postgresql-ha<br>
   Path: terraform-google-sql-db/examples/postgresql-ha<br>
 - Module: network-firewall-policy<br>
   Path: terraform-google-network/modules/network-firewall-policy<br>
 <br>
 **Remarks:** The postgresql module provides the core database functionality. The postgresql-public-iam example helps with IAM authentication similar to AD auth. The postgresql-ha example provides high availability features similar to geo-redundancy. The network-firewall-policy module helps implement network access rules similar to virtual network rules.<br>
<br>
### Module Mapping:<br>
 - Module: postgresql<br>
   Path: terraform-google-sql-db/modules/postgresql<br>
 <br>
 **Remarks:** The GCP PostgreSQL module provides equivalent functionality to the Azure PostgreSQL module, including high availability, backup configuration, security settings, and network access controls. While some features like Active Directory integration are handled differently in GCP (using Cloud IAM), the core database functionality, security features, and networking capabilities are well-matched. The GCP module supports similar configuration options for instance sizing, storage, backup retention, SSL enforcement, and network access rules.<br>
<br>
## azurerm_postgresql_db_server ```(./modules/azurerm_postgresql_db_server)``` <br>
### List of relevant modules:<br>
 - Module: postgresql<br>
   Path: terraform-google-sql-db/modules/postgresql<br>
 - Module: postgresql-ha<br>
   Path: terraform-google-sql-db/examples/postgresql-ha<br>
 - Module: network<br>
   Path: terraform-google-network/modules/vpc<br>
 - Module: firewall-rules<br>
   Path: terraform-google-network/modules/firewall-rules<br>
 <br>
 **Remarks:** The PostgreSQL module provides the core database functionality. The HA example demonstrates high-availability setup similar to geo-redundancy. VPC and firewall modules are needed for network access control similar to virtual_network_rule. For AD authentication, you'll need to implement Cloud IAM bindings using the database IAM users feature in Cloud SQL.<br>
<br>
### Module Mapping:<br>
 - Module: postgresql<br>
   Path: terraform-google-sql-db/modules/postgresql<br>
 - Module: network<br>
   Path: terraform-google-network/modules/vpc<br>
 - Module: firewall-rules<br>
   Path: terraform-google-network/modules/firewall-rules<br>
 <br>
 **Remarks:** The PostgreSQL module provides core database functionality including HA, backup, and security features. Network and firewall modules are needed to replicate the virtual network rules and access control functionality present in the source module. Note that GCP handles AD authentication differently through Cloud IAM, and threat detection is managed through Cloud SQL's built-in features rather than as a separate configuration.<br>
<br>
## azurerm_redis_cache ```(./modules/azurerm_redis_cache)``` <br>
### List of relevant modules:<br>
 - Module: memorystore-redis<br>
   Path: terraform-google-memorystore/modules/redis<br>
 - Module: redis-example<br>
   Path: terraform-google-memorystore/examples/redis<br>
 - Module: network-firewall-policy<br>
   Path: terraform-google-network/modules/network-firewall-policy<br>
 - Module: firewall-rules<br>
   Path: terraform-google-network/modules/firewall-rules<br>
 <br>
 **Remarks:** To replicate Azure Redis Cache functionality in GCP, you'll need both Memorystore (GCP's managed Redis service) and appropriate firewall configurations. The Memorystore module handles the Redis instance creation while the Network modules handle the firewall rules to control access to the Redis instance, similar to Azure's firewall rules functionality.<br>
<br>
### Module Mapping:<br>
 - Module: redis-example<br>
   Path: terraform-google-memorystore/examples/redis<br>
 - Module: firewall-rules<br>
   Path: terraform-google-network/modules/firewall-rules<br>
 <br>
 **Remarks:** The redis-example provides the core Redis/Memorystore functionality equivalent to azurerm_redis_cache, while the firewall-rules module handles the firewall rule configurations similar to azurerm_redis_firewall_rule. The redis example includes authentication, network access controls, and performance configurations matching the source module's capabilities. The firewall-rules module enables IP-based access control similar to the source module's firewall rules.<br>
<br>
## azurerm_storage_container ```(./modules/azurerm_storage_container)``` <br>
### List of relevant modules:<br>
 - Module: simple_bucket<br>
   Path: terraform-google-cloud-storage/modules/simple_bucket<br>
 - Module: storage_buckets_iam<br>
   Path: terraform-google-iam/modules/storage_buckets_iam<br>
 <br>
 **Remarks:** To replicate Azure Storage Container functionality in GCP, you'll need both the simple_bucket module for basic storage functionality and the storage_buckets_iam module to manage access controls. The simple_bucket module provides the core storage container functionality, while the storage_buckets_iam module handles the IAM permissions similar to Azure's access control.<br>
<br>
### Module Mapping:<br>
 - Module: simple_bucket<br>
   Path: terraform-google-cloud-storage/modules/simple_bucket<br>
 - Module: storage_buckets_iam<br>
   Path: terraform-google-iam/modules/storage_buckets_iam<br>
 <br>
 **Remarks:** The Azure Storage Container functionality can be replicated using GCP Storage Bucket modules. The simple_bucket module provides the core storage functionality, while the storage_buckets_iam module handles access control similar to Azure's container-level permissions. Note that GCP buckets are a higher-level construct than Azure containers, as Azure containers exist within storage accounts while GCP buckets are standalone resources.<br>
<br>
