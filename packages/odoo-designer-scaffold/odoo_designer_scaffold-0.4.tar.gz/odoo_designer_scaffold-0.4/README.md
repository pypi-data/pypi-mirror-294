# Odoo designer's Scaffold

This is a Python library for creating an Odoo.

## Installation

Use the package manager pip to install it.

```bash
pip install odoo_designer_scaffold
```

## Usage

```bash
# create your module with version and name (mandatory)
create-scaffold version_of_odoo module_name

create-scaffold 17.0 airproof


# create your module with more options
create-scaffold version_of_odoo module_name does_this_module_need_python number_of_website number_of_theme

create-scaffold 17.0 airproof True 2 1

```
