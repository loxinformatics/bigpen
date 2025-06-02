# Core Apps

This directory contains Django applications that form the **fundamental and universal backbone of all Tawala Bora projects**. They are part of our **standard project template**, providing essential functionalities required in every Django project we build.

These apps are designed to be stable, well-tested, and rarely modified on a project-specific basis. They represent the baseline features that every Tawala Bora solution starts with.

## Contents

You'll find applications here for common functionalities such as:

* Basic static pages and project-wide settings (`home`)
* Blogging functionality (`blog`)
* ...and other foundational components that establish the initial structure of a project.

## Guidelines

* **Universality:** These apps are intended to be included in every new project scaffolded from our template.
* **Stability:** Avoid making project-specific changes directly within these apps. If a change is needed, consider if it's a new universal feature that should be adopted across *all* future projects, or if it can be achieved via extension or configuration in a `custom` app.
* **Reusability:** Focus on keeping these apps generic and highly reusable.
* **Documentation:** Ensure that any new core app or significant changes to existing ones are well-documented for future use by any developer setting up a new project.

## When to modify

Modifications to `core` apps should generally only occur when:

* A new feature is universally required across all future projects built from this template.
* A bug fix is needed that applies to all implementations.
* An upgrade or refactor improves the general functionality without breaking existing projects.

For project-specific requirements or customizations, please create or modify apps within the `custom` directory.