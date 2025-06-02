# Custom Apps

This directory houses Django applications that are **specific to individual client requirements or unique project functionalities**.

Unlike `core` apps, these applications are designed to address particular business logic, unique features, or client-specific integrations that are not universally required across all our projects. They are built on top of the `core` foundation to deliver tailored solutions.

## Contents

You'll find applications here that might include:

* E-commerce functionalities (`shop`)
* Educational platform features (`school`)
* Church management systems (`church`)
* Any bespoke features or integrations tailored for a specific client.

## Guidelines

* **Project-Specific:** Each app in this directory should typically serve a unique need for a single project or client.
* **Flexibility:** These apps are where the majority of project-specific development and customization takes place.
* **Dependencies:** While `custom` apps can depend on `core` apps, `core` apps should generally not depend on `custom` apps to maintain their universal nature and reusability as part of the template.
* **Naming:** Use clear, descriptive names for your custom apps that reflect their specific purpose (e.g., `client_x_crm`, `project_y_dashboard`).

## When to create/modify

* When a new project requires functionality not present in `core` apps.
* When existing `core` app functionality needs to be extended or overridden for a specific project.
* When integrating with third-party services unique to a particular client.

Before creating a new `custom` app, consider if the functionality might genuinely be universally useful. If so, discuss whether it could be a candidate for a new `core` app to be added to the standard project template.