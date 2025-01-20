# Django Multi-Vendor Application

Welcome to the Django Multi-Vendor Application! This project is designed for managing users, vendors, and various data privacy and segmentation functionalities, with a focus on compliance with major data privacy laws like GDPR, CCPA, DPDP Act (India), and others.

## Project Overview

- **Project Name**: Core
- **Apps**: 
  - `user`: Manages user profiles, permissions, and authentication.
  - `shared`: Contains models that are shared across the application.

## Key Features

- **User Segmentation**: Based on demographics, behavior, geographic location, and psychographics.
- **Timezone and Currency Handling**: Supports multi-timezone and currency operations.
- **Tax Management**: Configurable tax systems per state.
- **Vendor Management**: Vendor-specific fields and operations.
- **Data Privacy Compliance**: Features to comply with GDPR, CCPA, and other data protection laws.

## Models

### User Models

- **CustomUser**:
  - Includes user-specific fields like `user_type`, `unique_id`, `country`, `state`, `city`.
  - **Compliance Fields**:
    - `income_level`: For demographic segmentation, consider privacy implications.
    - `housing_status`: Helps in income estimation but sensitive under privacy laws.
    - `postal_code`: Useful for geographic segmentation and compliance, must be handled with privacy in mind.

### Privacy and Compliance Models

- **UserPrivacySettings**:
  - **Purpose**: To handle state-specific privacy settings in the US.
  - **Fields**:
    - `can_sell_data`, `can_target_ads`, `can_share_data`: Boolean fields to manage user data rights under various state laws.

- **PrivacyByDesign**:
  - **Purpose**: To incorporate Privacy by Design principles, particularly relevant for Canadian compliance.
  - **Fields**:
    - `privacy_notice_accepted`: Tracks user acceptance of privacy notices.
    - `data_minimized`: JSON field to note which data is minimized.

- **IndianUserData**:
  - **Purpose**: Compliance with the Indian DPDP Act.
  - **Fields**:
    - `consent_for_processing`: Tracks user consent for data processing.
    - `data_purpose`: Describes the purpose for which data is being collected.
    - `data_lifecycle`: JSON field to manage data retention policies.

- **GDPRCompliance**:
  - **Purpose**: To manage GDPR rights implementation.
  - **Fields**:
    - `has_access_right`, `has_rectification_right`, `has_erase_right`, `has_portability_right`: Flags to manage GDPR data subject rights.

- **EncryptedData**:
  - **Purpose**: For storing sensitive data securely across all jurisdictions.
  - **Fields**:
    - `encrypted_content`: Stores encrypted data.
    - `encryption_method`: Describes the method used for encryption.

## Compliance Considerations

### GDPR

- **User Rights**: Implement views or APIs to handle:
  - Access (view data)
  - Rectification (update data)
  - Erasure (delete data)
  - Restriction of Processing
  - Data Portability
  - Object to Processing
  - Control over automated decisions

### CCPA

- **Consumer Rights**: Similar to GDPR but with specific requirements for California residents:
  - Right to know what personal information is collected.
  - Right to delete personal information.
  - Right to opt-out of sale of personal information.

### Canadian Privacy Laws

- **Privacy by Design**: Integrate privacy from the start of your data lifecycle.

### Indian DPDP Act

- **Consent Management**: Ensure explicit consent for data processing with clear data purposes.

## Development & Compliance Tips

- **Data Minimization**: Collect only what is necessary.
- **Transparent Consent**: Use clear language when asking for consent.
- **Regular Audits**: Ensure your practices align with the latest privacy law amendments.
- **Encryption**: Use strong encryption for sensitive data, manage keys securely.
- **Audit Logs**: Keep logs of data access and changes for compliance audits.

## Setup

1. **Clone the Repository**: