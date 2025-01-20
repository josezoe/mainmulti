Admin Interface Documentation
Overview
This document outlines the administration interface setup for the Django application, focusing on user management, vendor management, and compliance with privacy regulations.

Admin Models
CustomUser
Description: Main user model with additional fields for user segmentation, behavior analytics, and privacy compliance.
Admin Features:
List Display: Shows key metrics like engagement scores, retention status, lifetime value, etc.
Search Fields: Allows searching by username, email, phone, and geographic details.
List Filters: Includes custom filters for location, date range, and cohorts.
Inlines: 
UserPrivacySettings
PrivacyByDesign
IndianUserData
GDPRCompliance
UserConsent
Custom Methods: Calculate various user metrics and statistics.

Vendor
Description: Represents vendor profiles with additional business-related fields.
Admin Features:
List Display: Focuses on vendor-specific information like company name, ratings, and location.
Search Fields: Similar to CustomUser but includes vendor-specific data.
List Filters: Location, cuisine type, creation date, and date range.

UserPrivacySettings
Description: Manages user privacy preferences for compliance with privacy laws like CCPA.
Admin Integration: Managed inline within CustomUser admin.

PrivacyByDesign
Description: Ensures privacy by design principles are followed, mainly for Canadian privacy compliance.
Admin Integration: Managed inline within CustomUser admin.

IndianUserData
Description: Specific data for compliance with the Indian DPDP Act.
Admin Integration: Managed inline within CustomUser admin.

GDPRCompliance
Description: Manages user rights under GDPR.
Admin Integration: Managed inline within CustomUser admin.

UserConsent
Description: Tracks consents given by users for various data uses.
Admin Integration: Managed inline within CustomUser admin.

ConsentType
Description: Defines categories of consent that users can give or withdraw.
Admin Features:
List Display: Shows consent type names and descriptions.
Search Fields: Allows searching by consent type name or description.

Custom Filters
DateRangeFilter: Filter users or vendors based on their last interaction date.
Options: Today, Yesterday, This Week, Last Week, This Month, Last Month, Custom Range.
LocationFilter: Hierarchical filter by country, state, and city.
CohortFilter: Filter users by their registration cohort for retention analysis.

Admin Methods
get_summary_data: Compiles and caches summary statistics.
get_engagement_stats: Calculates engagement metrics.
get_retention_stats: Computes retention statistics.
get_ltv_stats: Estimates user Lifetime Value (LTV).
get_session_stats: Analyzes session length data.
get_nps_stats: Aggregates Net Promoter Score (NPS) data.
get_cohort_stats: Provides cohort-based performance metrics.
get_churn_stats: Calculates churn rates.
display_summary: Formats and displays all computed metrics in HTML.

Usage Considerations
Privacy and Compliance: Handle data with care, ensuring compliance with privacy laws. Limit access to sensitive data based on admin privileges.
Performance: Large datasets might slow down the admin interface. Use caching and consider pagination for inlines.
Security: Ensure that all admin users have appropriate permissions and that the interface is secure against unauthorized access.

Future Enhancements
Visual Analytics: Add graphical representations of data for easier analysis.
Bulk Actions: Introduce bulk operations for privacy settings or consent management.
Audit Trails: Implement logging for changes in user data or privacy settings.
Custom Dashboards: Create or extend admin views to serve as dashboards for key metrics.

This setup provides a robust admin interface for managing users, vendors, and ensuring compliance with various data privacy laws, with tools for deep analysis of user behavior and retention.