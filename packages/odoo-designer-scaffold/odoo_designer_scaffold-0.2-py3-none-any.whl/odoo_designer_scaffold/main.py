import sys

from io import BytesIO
from zipfile import ZipFile
from PIL import Image

def create_zip(zip_file, name, version, with_python, website_number, theme_number):
    
    if with_python:
        compute_name = 'website_%s_backend' % (name)
        python_manifest = create_python_module_manifest(zip_file, compute_name, version)
        zip_file.writestr(compute_name+'/__manifest__.py', python_manifest)
        zip_file.writestr(compute_name+'/__init__.py', '# -*- coding: utf-8 -*-')
        zip_file.writestr(compute_name+'/models/__init__.py', '# -*- coding: utf-8 -*-')
        zip_file.writestr(compute_name+'/tests/','')

    if website_number == 1 :
        compute_name = 'website_%s' % (name)
        create_website_module(zip_file, compute_name, version)
    else:
        while website_number > 0:
            compute_name = 'website_%s_%s' % (name,website_number)
            create_website_module(zip_file, compute_name, version)
            website_number -= 1

    if theme_number == 1 :
        compute_name = 'theme_%s' % (name)
        create_theme_module(zip_file, compute_name, version)
    else:
        while theme_number > 0:
            compute_name = 'theme_%s_%s' % (name,theme_number)
            create_theme_module(zip_file, compute_name, version)
            theme_number -= 1

def create_website_module(zip_file, name, version):
    manifest_file = create_module_manifest(name, version)
    zip_file.writestr(name+'/__manifest__.py',manifest_file)
    zip_file.writestr(name+'/__init__.py', '# -*- coding: utf-8 -*-')
    zip_file.writestr(name+'/controllers/__init__.py', '# -*- coding: utf-8 -*-')
    create_module_static_files(zip_file, name)

def create_theme_module(zip_file, name, version):
    manifest_file = create_theme_manifest(name, version)
    zip_file.writestr(name+'/__manifest__.py',manifest_file)
    create_theme_static_files(zip_file, name)

def create_module_manifest(name, version):
    return """{
        'name': '"""+name+"""',
        'version': '"""+version+""".0.0',
        'depends': ['website'],
        'license': 'LGPL-3',
        'data': [
            # Images
            'data/images.xml',
            # Menu
            'data/menu.xml',
            # Presets
            'data/presets.xml',
            # Static pages
            'data/pages/home.xml',
            # Views 
            'views/website_templates.xml'
        ],
        'assets': {
            'web.assets_frontend': [
                # Global QWeb JS Templates
                '"""+name+"""/static/src/xml/example.xml',
               
            ],
        },
        'cloc_exclude': [
            'lib/**/*',
            'data/**/*'
        ],
    }"""

def create_theme_manifest(name, version):
    return """{
        'name': '"""+name+"""',
        'version': '"""+version+""".0.0',
        'depends': ['website'],
        'license': 'LGPL-3',
        'data': [
            # Views
            'views/snippets/options.xml',
            'views/snippets/s_wd_snippet.xml',
        ],
        'assets': {
            'web._assets_primary_variables': [
                '"""+name+"""/static/src/scss/primary_variables.scss',
            ],
            'web._assets_frontend_helpers': [
                ('prepend', '"""+name+"""/static/src/scss/bootstrap_overridden.scss'),
            ],
            'web.assets_frontend': [
                # LIB
                # Lib name
                # '"""+name+"""/static/src/lib/libname/libname.min.css',
                # '"""+name+"""/static/src/lib/libname/libname.min.js', 
                # SCSS
                # Base
                '"""+name+"""/static/src/scss/base/variables.scss',
                '"""+name+"""/static/src/scss/base/functions.scss',
                '"""+name+"""/static/src/scss/base/mixins.scss',
                #'"""+name+"""/static/src/scss/base/fonts.scss',
                '"""+name+"""/static/src/scss/base/icons.scss',
                '"""+name+"""/static/src/scss/base/helpers.scss',
                '"""+name+"""/static/src/scss/base/typography.scss',
                # Components
                #'"""+name+"""/static/src/scss/components/*.scss',
                # Layout
                '"""+name+"""/static/src/scss/layout/body.scss',
                '"""+name+"""/static/src/scss/layout/header.scss',
                '"""+name+"""/static/src/scss/layout/footer.scss',
                '"""+name+"""/static/src/scss/layout/blog.scss',
                # Pages
                '"""+name+"""/static/src/scss/pages/home.scss',
                # Standard Snippets Overrides
                '"""+name+"""/static/src/scss/snippets/cookies_bar.scss',
                # Custom Snippets
                #'"""+name+"""/static/src/snippets/s_wd_snippet/000.scss',
                #'"""+name+"""/static/src/snippets/s_wd_snippet/000.xml',
                #'"""+name+"""/static/src/snippets/s_wd_snippet/000.js',
            ],
            'website.assets_wysiwyg': [
                '"""+name+"""/static/src/snippets/s_wd_snippet/options.js'
            ]
        },
        'cloc_exclude': [
            'static/src/scss/bootstrap_overridden.scss',
            'static/src/scss/primary_variables.scss',
            'lib/**/*',
            'data/**/*'
        ],
    }"""

def create_python_module_manifest(zip_file, name, version):
    return """{
        'name': '"""+name+"""',
        'version': '"""+version+"""0.0',
        'depends': [],
        'license': 'LGPL-3',
        'data': [],
        'assets': {},
    }"""

def create_theme_static_files(zip_file, name):
    bootstrap = """// Override any bootstrap variable from here.

    $grid-gutter-width: 30px;
    $enable-rfs: true;"""

    bootsrap_latest ="""/// As the number of lines of code can be critic: 
    // Feel free to just extend the utility classes manually (without Bootstrap Utilities API and boostrap_utilities.scss).
    // Newly created variables have to be located in the base/variables.scss as this is the first SCSS file called.

    // Classes
    // .fw-medium { font-weight: $font-weight-medium; }
    // .fw-semibold { font-weight: $font-weight-semibold; }"""

    functions = """// ------------------------------------------------------------------------------ //
    // FUNCTIONS - (Only return/compute values, no CSS selectors output)
    // ------------------------------------------------------------------------------ //

    /**
    * Explanation of your function
    *
    * @param {Type} $variable - Explanation about this variable
    * 
    * Usage:
    * @include my-function($variable);
    */
    /*
    @function my-function($variable: default) {
        @return $result;
    }
    */"""

    helpers = """// ------------------------------------------------------------------------------ //
    // HELPERS - (Global classes used across the whole website)
    // ------------------------------------------------------------------------------ //"""

    icons = """// ------------------------------------------------------------------------------ //
    // ICONS - Custom Icon Font Set
    // ------------------------------------------------------------------------------ //

    /*
    @font-face {
        font-family: 'scaffold-icons';
        src: url('../../fonts/scaffold-icons.woff?wyfr5p') format('woff');
        font-weight: normal;
        font-style: normal;
        font-display: block;
    }

    .x_wd_icon {
        // Use !important to prevent issues with browser extensions that change fonts
        font-family: 'materrup-icons' !important;
        speak: never;
        font-style: normal;
        font-weight: normal;
        font-variant: normal;
        text-transform: none;
        line-height: 1;

        // Better Font Rendering
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .x_wd_icon_arrow_left:before { content: '\f001'; }
    */"""

    mixins = """// ------------------------------------------------------------------------------ //
    // MIXINS
    // ------------------------------------------------------------------------------ //

    /**
    * Explanation of your mixin
    *
    * @param {Type} $variable - Explanation about this variable
    * 
    * Usage:
    * @include my-mixin($variable);
    */
    /*
    @mixin my-mixin($variable: default) {


    }
    */"""

    placeholders = """// ------------------------------------------------------------------------------ //
    // PLACEHOLDERS - All %placeholder declarations
    // ------------------------------------------------------------------------------ //"""

    typography = """// ------------------------------------------------------------------------------ //
    // TYPOGRAPHY - Everything related to font style helpers (headings, font-weights, etc)
    // ------------------------------------------------------------------------------ //

    strong, b {}
    em, i {}"""

    variables = """// ------------------------------------------------------------------------------ //
    // VARIABLES - Custom SASS and CSS Variables
    // ------------------------------------------------------------------------------ //

    // Set your global SASS variable here:
    // $custom-sass-variable: value;

    :root {
        // Set your CSS variables here: 
        // --my-variable: value;
    }"""

    blog = """// ------------------------------------------------------------------------------ //
    // WEBSITE BLOG - Styles used on multiple views within the blog App.
    // ------------------------------------------------------------------------------ //
    #wrap.website_blog {

    }"""

    body = """// ------------------------------------------------------------------------------ //
    // BODY
    // ------------------------------------------------------------------------------ //
    body {
        // For exemaple: 
        // -webkit-font-smoothing: antialiased;
        // -moz-osx-font-smoothing: grayscale;
    }"""

    footer = """// ------------------------------------------------------------------------------ //
    // FOOTER
    // ------------------------------------------------------------------------------ //
    .x_wd_footer {

    }"""

    header = """// ------------------------------------------------------------------------------ //
    // HEADER
    // ------------------------------------------------------------------------------ //
    .x_wd_header {

    }"""

    home_scss = """// ------------------------------------------------------------------------------ //
    // HOME PAGE
    // ------------------------------------------------------------------------------ //
    .x_wd_page_home {

    }"""

    cookies_bar = """// ------------------------------------------------------------------------------ //
    // STANDARD SNIPPET - Minor style changes of existing snippet
    // ------------------------------------------------------------------------------ //"""

    snippet_scss = """.s_wd_snippet {
        
    }"""

    snippet_xml = """<?xml version="1.0" encoding="utf-8"?>
    <templates>
        <t t-name=\""""+name+""".s_wd_snippet">
            <!-- Your markup here -->
        </t>
    </templates>"""

    s_wd_snippet = """<?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <template id="s_wd_snippet" name="Custom Snippet">
            <section class="s_wd_snippet o_cc o_cc1 pt48 pb48">
                <div class="container s_allow_columns">
                    <!-- Your content here -->
                    <h1 class="text-center display-1">Welcome</h1>
                    <p class="text-center">Hello my dear Odooer!</p>
                    <br />
                    <img src="/web/image/"""+name+""".img_s_wd_snippet_default" class="img img-fluid mx-auto d-block text-center" alt="Default Image" />
                </div>
            </section>
        </template>
    </odoo>"""

    primary_var="""// ------------------------------------------------------------------------------ //
    // PRESETS
    // ------------------------------------------------------------------------------ //
    $o-website-values-palettes: (
        (
            // Colors
            'color-palettes-name':              '"""+name+"""',

            // Fonts
            'font':                             'Inter',
            'headings-font':                    'Caveat',
            'navbar-font':                      'Inter',
            'buttons-font':                     'Inter',

            // Header
            'header-template':                  '"""+name+"""',
            'header-font-size':                 1rem,
            'logo-height':                      1.5rem,
            'fixed-logo-height':                1rem,

            // Footer
            'footer-template':                  '"""+name+"""'
        ),
    );

    // ------------------------------------------------------------------------------ //
    // FONTS
    // ------------------------------------------------------------------------------ //
    $o-theme-font-configs: (
        'Caveat': (
            'family':   ('Caveat', cursive),
            'url':      'Caveat:400,500,700',
            'properties' : (
                'base': (
                    'font-size-base': 1rem
                )
            )
        ),
        'Inter': (
            'family':   ('Inter', sans-serif),
            'url':      'Inter:400,400i,500,500i,700,700i',
            'properties': (
                'base': (
                    'font-size-base': 1rem
                )
            )
        ),
    );

    // ------------------------------------------------------------------------------ //
    // COLORS
    // ------------------------------------------------------------------------------ //
    $o-color-palettes: map-merge($o-color-palettes,
        (
            'Scaffold': (
                'o-color-1': #714B67, // Primary
                'o-color-2': #017E84, // Secondary
                'o-color-3': #F3F4F6, // Light
                'o-color-4': #FFFFFF, // Whitish
                'o-color-5': #111827, // Blackish

                'menu':        2,
                'footer':      5
            )
        )
    );

    $o-user-gray-color-palette: (
        'white': #FFFFFF,
        '100':   #E6E7E8,
        '200':   #D1D2D4,
        '300':   #BCBDBF,
        '400':   #A8A9AC,
        '500':   #949598,
        '600':   #818285,
        '700':   #6D6E71,
        '800':   #58585A,
        '900':   #3A3A3B,
        'black': #292929
    );

    $o-user-theme-color-palette: (
        'success': #00C35A,
        'danger':  #D72F3D,
        'warning': #FFB82A, 
        'info':    #2F72D7,
        'light':   #FFF2E9,
        'dark':    #505050
    );"""

    option = """<?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <!-- Add custom snippets -->
        <template id="snippets" inherit_id="website.snippets" name="Scaffold - Snippets">
            <xpath expr="//*[@id='default_snippets']" position="before">
                <t id="x_wd_snippets">
                    <div id="x_snippets_category_static" class="o_panel">
                        <div class="o_panel_header">Scaffold</div>
                        <div class="o_panel_body">
                            <t t-snippet=\""""+name+""".s_wd_snippet" t-thumbnail="/"""+name+"""/static/src/img/wbuilder/snippet_thumbnail.svg">
                                <keywords>Custom, Snippet</keywords>
                            </t>
                        </div>
                    </div>
                </t>
            </xpath>
        </template>

        <!-- Website builder: Global options -->
        <template id="snippet_options" inherit_id="website.snippet_options" name="Scaffold - Snippets Options">
            <!-- Insert your options here within an Xpath -->
        </template>
    </odoo>"""

    theme="""#wrapwrap {  
        > header {}
        > main {}
        > footer {}
    }"""

    # Style    
    zip_file.writestr(name+'/static/src/scss/bootstrap_overridden.scss',bootstrap)
    zip_file.writestr(name+'/static/src/scss/bootstrap_latest.scss',bootsrap_latest)
    zip_file.writestr(name+'/static/src/scss/primary_variables.scss',primary_var)
    zip_file.writestr(name+'/static/src/scss/theme.scss',theme)
        # Base
    zip_file.writestr(name+'/static/src/scss/base/functions.scss',functions)
    zip_file.writestr(name+'/static/src/scss/base/helpers.scss',helpers)
    zip_file.writestr(name+'/static/src/scss/base/icons.scss',icons)
    zip_file.writestr(name+'/static/src/scss/base/mixins.scss',mixins)
    zip_file.writestr(name+'/static/src/scss/base/placeholders.scss',placeholders)
    zip_file.writestr(name+'/static/src/scss/base/typography.scss',typography)
    zip_file.writestr(name+'/static/src/scss/base/variables.scss',variables)
        # Layout
    zip_file.writestr(name+'/static/src/scss/layout/blog.scss',blog)
    zip_file.writestr(name+'/static/src/scss/layout/body.scss',body)
    zip_file.writestr(name+'/static/src/scss/layout/footer.scss',footer)
    zip_file.writestr(name+'/static/src/scss/layout/header.scss',header)
        # Pages
    zip_file.writestr(name+'/static/src/scss/pages/home.scss',home_scss)
        # Snippets
    zip_file.writestr(name+'/static/src/scss/snippets/cookies_bar.scss',cookies_bar)
    zip_file.writestr(name+'/views/snippets/options.xml',option)

    # Snippets
    zip_file.writestr(name+'/static/src/scss/snippets/s_wd_snippet/000.js','')
    zip_file.writestr(name+'/static/src/scss/snippets/s_wd_snippet/000.scss',snippet_scss)
    zip_file.writestr(name+'/static/src/scss/snippets/s_wd_snippet/000.xml',snippet_xml)
    zip_file.writestr(name+'/static/src/scss/snippets/s_wd_snippet/options.js','')

    # Views
    zip_file.writestr(name+'/views/snippets/s_wd_snippet.xml',s_wd_snippet)

def create_module_static_files(zip_file, name):
    home = """<?xml version="1.0" encoding="utf-8"?>
    <odoo noupdate="1">
        <record id="page_home" model="website.page">
            <field name="name">Home</field>
            <field name="is_published" eval="True" />
            <field name="key">"""+name+""".page_home</field>
            <field name="url">/</field>
            <field name="type">qweb</field>
            <field name="website_id" eval="1" />
            <field name="arch" type="xml">
                <t name="Accueil" t-name=\""""+name+""".page_home">
                    <t t-call="website.layout">
                        <!-- <title> in the <head> -->
                        <t t-set="additional_title" t-valuef="Home" />
                        <!-- body classes -->
                        <t t-set="pageName" t-valuef="x_wd_page_home" />

                        <div id="wrap" class="oe_structure">
                            <!-- Your building blocks here -->
                            <section class="s_wd_snippet o_cc o_cc1 pt48 pb48" data-snippet="s_wd_snippet" data-name="Custom Snippet">
                                <div class="container s_allow_columns">
                                    <h1 class="text-center display-1">Welcome</h1>
                                    <p class="text-center">Hello my dear Odooer!</p>
                                    <br />
                                    <img src="/web/image/"""+name+""".img_s_wd_snippet_default" class="img img-fluid mx-auto d-block text-center" alt="Default Image" />
                                </div>
                            </section>
                        </div>
                    </t>
                </t>
            </field>
        </record>
    </odoo>"""

    menu = """<?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <!-- Default Homepage
        <delete model="website.menu" search="[('url','in', ['/', '/']), ('website_id', '=', 1)]"/>

        <record id="menu_example" model="website.menu">
            <field name="name">Example</field>
            <field name="url">/example</field>
            <field name="parent_id" search="[
                ('url', '=', '/default-main-menu'),
                ('website_id', '=', 1)]"/>
            <field name="website_id">1</field>
            <field name="sequence" type="int">20</field>
        </record> 
        -->
    </odoo>"""

    images= """<?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <!-- Branding -->
        <record id="logo" model="ir.attachment">
            <field name="name">Logo</field>
            <field name="datas" type="base64" file=\""""+name+"""/static/src/img/content/logo.svg"/>
            <field name="res_model">ir.ui.view</field>
            <field name="public" eval="True"/>
        </record>

        <record id="website.default_website" model="website">
            <field name="logo" type="base64" file=\""""+name+"""/static/src/img/content/logo.svg"/>
        </record>

        <!-- Snippets -->
        <record id="img_s_wd_snippet_default" model="ir.attachment">
            <field name="name">Default Custom Snippet Image</field>
            <field name="datas" type="base64" file=\""""+name+"""/static/src/img/content/snippets/s_wd_snippet/default.gif"/>
            <field name="res_model">ir.ui.view</field>
            <field name="public" eval="True"/>
        </record>
    </odoo>
    """

    presets = """<?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <!-- Disable default header template -->
        <record id="website.template_header_default" model="ir.ui.view">
            <field name="active" eval="False"/>
        </record>
        <!-- Default pages -->
        <!-- Disable Default Home -->
        <record id="website.homepage" model="ir.ui.view">
            <field name="active" eval="False"/>
        </record>
    </odoo>
    """

    

    template_wbuilder_opt = """<?xml version="1.0" encoding="UTF-8"?><svg id="uuid-a9541345-95cf-401e-b2c8-d4bb13d2b6f1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 234 60" width="234" height="60"><defs><clipPath id="uuid-3bcc0ef0-40a5-4efa-aa43-5e471cefb0ae"><rect x="60" y="11.54" width="114" height="36.96" fill="none" stroke-width="0"/></clipPath></defs><g clip-path="url(#uuid-3bcc0ef0-40a5-4efa-aa43-5e471cefb0ae)"><path d="M159.22,28.27c4.65.65,14.17,2.7,14.2-6.33,0-.47-.36-.34-.57-.14-5.55,5.34-7.38,0-15.28,0-6.42,0-11.85,4.29-11.85,11.95s5.19,11.95,11.85,11.95,11.85-4.06,11.85-11.95c0-1.3-.13-2.5-.41-3.59-.07-.27-.25-.33-.5-.28-.81.16-1.71.24-2.68.24-1.23,0-2.46-.12-3.64-.27-.18-.02-.37.12-.17.43.55.85.91,1.98.91,3.47,0,4.34-2.99,5.7-5.36,5.7s-5.36-1.39-5.36-5.7,3.63-5.95,7.01-5.48Z" fill="#fff" fill-rule="evenodd" stroke-width="0"/><path d="M145.73,41.82c-.25-.05-1.13-.05-1.38,0-4.22.81-1.04,6.48.69,6.48s4.91-5.67.69-6.48Z" fill="#fff" fill-rule="evenodd" stroke-width="0"/><path d="M131.02,28.27c-4.65.65-14.17,2.7-14.2-6.33,0-.47.36-.34.57-.14,5.55,5.34,7.38,0,15.28,0,6.42,0,11.85,4.29,11.85,11.95s-5.19,11.95-11.85,11.95-11.85-4.06-11.85-11.95c0-1.3.13-2.5.41-3.59.07-.27.25-.33.5-.28.81.16,1.7.24,2.68.24,1.23,0,2.46-.12,3.64-.27.18-.02.37.12.17.43-.56.85-.91,1.98-.91,3.47,0,4.34,2.99,5.7,5.36,5.7s5.36-1.39,5.36-5.7-3.62-5.95-7.01-5.48Z" fill="#fff" fill-rule="evenodd" stroke-width="0"/><path d="M118.83,33.58c0,7.44-5.3,12.12-11.96,12.12s-11.85-4.29-11.85-11.95V13.32c0-.51.45-.96.96-.96h4.63c.51,0,.96.45.96.96v11.01c2.14-2.31,5.13-2.54,6.77-2.54,7,.28,10.49,5.64,10.49,11.79ZM112.34,33.75c0-4.06-2.93-5.75-5.3-5.75s-5.47,1.41-5.47,5.7,2.93,5.81,5.3,5.81,5.47-1.69,5.47-5.75Z" fill="#fff" fill-rule="evenodd" stroke-width="0"/><path d="M88.63,19.44c-2.2,0-3.95-1.75-3.95-3.95s1.75-3.95,3.95-3.95,3.95,1.75,3.95,3.95-1.75,3.95-3.95,3.95ZM91.9,44.07c0,.51-.45.96-.96.96h-4.63c-.51,0-.96-.45-.96-.96v-20.64c0-.51.45-.96.96-.96h4.63c.51,0,.96.45.96.96v20.64Z" fill="#fff" fill-rule="evenodd" stroke-width="0"/><path d="M82.34,33.07v11c0,.51-.45.96-.96.96h-4.63c-.51,0-.96-.45-.96-.96v-11c0-2.88-1.41-5.02-4.63-5.02s-4.63,2.14-4.63,5.02v11c0,.51-.45.96-.96.96h-4.63c-.51,0-.96-.45-.96-.96v-11c0-7.5,4.91-11.28,11.17-11.28s11.17,3.78,11.17,11.28Z" fill="#fff" fill-rule="evenodd" stroke-width="0"/></g><path d="M234,0v60H0V0" fill="#aaa6d2" fill-rule="evenodd" stroke-width="0"/><path id="uuid-f13ff652-44ef-4128-930f-06fe73b2c155" d="M145.31,60l13.41-20.78-12.27-27.39h-15.83l-8.18,9.13-8.89-9.13-8.3,11.32-13.22-11.32-8.95,10.91.41-10.91h-12.86l-32.19,48.17h106.86Z" fill="#3a3a39" isolation="isolate" opacity=".12" stroke-width="0"/><path d="M126.48,11.83l-15.41,36.34h-14.82l-.59-20.63-8.18,20.63h-14.82l-1.96-36.34h12.8l-.77,22.88,9.31-22.88h12.98l.89,22.88,7.65-22.88h12.92Z" fill="#fff" stroke-width="0"/><path d="M155.59,13.67c2.49,1.19,4.39,2.9,5.75,5.1,1.3,2.19,1.96,4.68,1.96,7.53,0,1.13-.12,2.37-.3,3.62-.65,3.44-2.02,6.58-4.15,9.37-2.13,2.79-4.8,4.98-8.12,6.52-3.26,1.6-6.88,2.37-10.85,2.37h-15.83l6.7-36.34h15.83c3.5,0,6.52.59,9.01,1.84ZM147.47,35.9c1.84-1.42,2.96-3.38,3.44-5.99.12-.71.18-1.3.18-1.9,0-2.02-.65-3.56-1.96-4.62s-3.14-1.6-5.45-1.6h-2.85l-3.02,16.24h2.85c2.73-.06,4.98-.71,6.82-2.13Z" fill="#fff" stroke-width="0"/></svg>"""

    snippet_thumbnail = """<?xml version="1.0" encoding="UTF-8"?><svg id="uuid-1763626b-30ae-4377-a919-bbb8da050104" xmlns="http://www.w3.org/2000/svg" width="240" height="180" viewBox="0 0 240 180"><g id="uuid-b048a4a2-c32e-4dc6-8f93-acf0d184184d"><path d="M0,0h240v180H0V0Z" fill="#aaa6d2" fill-rule="evenodd" stroke-width="0"/></g><polygon points="169.8 59.35 143.1 59.35 129.3 74.75 114.3 59.35 100.3 78.45 78 59.35 62.9 77.75 63.6 59.35 41.9 59.35 0 122.05 0 180 142.44 180 190.5 105.55 169.8 59.35" fill="#3a3a39" isolation="isolate" opacity=".12" stroke-width="0"/><path d="M136,59.35l-26,61.3h-25l-1-34.8-13.8,34.8h-25l-3.3-61.3h21.6l-1.3,38.6,15.7-38.6h21.9l1.5,38.6,12.9-38.6h21.8Z" fill="#fff" stroke-width="0"/><path d="M185.1,62.45c4.2,2,7.4,4.9,9.7,8.6,2.2,3.7,3.3,7.9,3.3,12.7,0,1.9-.2,4-.5,6.1-1.1,5.8-3.4,11.1-7,15.8-3.6,4.7-8.1,8.4-13.7,11-5.5,2.7-11.6,4-18.3,4h-26.7l11.3-61.3h26.7c5.9,0,11,1,15.2,3.1ZM171.4,99.95c3.1-2.4,5-5.7,5.8-10.1.2-1.2.3-2.2.3-3.2,0-3.4-1.1-6-3.3-7.8s-5.3-2.7-9.2-2.7h-4.8l-5.1,27.4h4.8c4.6-.1,8.4-1.2,11.5-3.6Z" fill="#fff" stroke-width="0"/></svg>"""

    logo = """<?xml version="1.0" encoding="utf-8"?>
    <!-- Generator: Adobe Illustrator 24.3.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
    <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        viewBox="0 0 126.2 40" style="enable-background:new 0 0 126.2 40;" xml:space="preserve">
    <style type="text/css">
        .st0{fill:#8F8F8F;}
        .st1{fill:#714B67;}
    </style>
    <g id="Group_982" transform="translate(-13.729 -4.35)">
        <path id="Path_172" class="st0" d="M60.9,38c4.9,0,8.9-4,8.9-8.9c0-4.9-4-8.9-8.9-8.9c-4.9,0-8.9,4-8.9,8.9c0,0,0,0,0,0
            C51.9,34,55.9,38,60.9,38 M76.1,28.8c0.1,8.4-6.6,15.4-15,15.5c-8.4,0.1-15.4-6.6-15.5-15c0-0.2,0-0.3,0-0.5
            c0.3-8.6,7.6-15.4,16.2-15.1c2.9,0.1,5.6,1,8,2.6V7.4c0.1-1.7,1.5-3.1,3.3-3.1c1.7,0,3,1.4,3.1,3.1L76.1,28.8z M92.7,38
            c4.9,0,8.9-4,8.9-8.9c0-4.9-4-8.9-8.9-8.9c-4.9,0-8.9,4-8.9,8.9c0,0,0,0,0,0C83.8,34,87.8,38,92.7,38L92.7,38 M92.7,44.3
            c-8.4,0-15.2-6.8-15.2-15.2c0-8.4,6.8-15.2,15.2-15.2c8.4,0,15.2,6.8,15.2,15.2c0,0,0,0,0,0C108,37.4,101.2,44.3,92.7,44.3
            M124.6,38c4.9,0,8.9-4,8.9-8.9s-4-8.9-8.9-8.9c-4.9,0-8.9,4-8.9,8.9c0,0,0,0,0,0C115.7,34,119.7,38,124.6,38 M124.6,44.3
            c-8.4,0-15.2-6.8-15.2-15.2c0-8.4,6.8-15.2,15.2-15.2c8.4,0,15.2,6.8,15.2,15.2c0,0,0,0,0,0C139.9,37.4,133,44.3,124.6,44.3"/>
        <path id="Path_173" class="st1" d="M29,38c4.9,0,8.9-4,8.9-8.9c0-4.9-4-8.9-8.9-8.9c-4.9,0-8.9,4-8.9,8.9c0,0,0,0,0,0
            C20,34,24,38,29,38 M29,44.3c-8.4,0-15.2-6.8-15.2-15.2S20.5,13.8,29,13.8S44.2,20.6,44.2,29c0,0,0,0,0,0
            C44.2,37.4,37.4,44.3,29,44.3C29,44.3,29,44.3,29,44.3"/>
    </g>
    </svg>"""

    xml_example = """<?xml version="1.0" encoding="utf-8"?>
    <templates>
        <!-- If you need to call global QWeb JS templates through a global JS file (/static/src/js), this is how/where you can declare it.  -->
        <t t-name=\""""+name+""".x_wd_example">
            <!-- Your markup here -->
        </t>
    </templates>"""

    website_templates = """<?xml version="1.0" encoding="utf-8" ?>
    <odoo>
        <!-- [ CUSTOM HEADER ]-->
        <!-- =================================== -->

        <!-- [ TEMPLATE: HEADER OPT ]-->
        <template id="template_header_opt" inherit_id="website.snippet_options" name=" Scaffold Header Template - Option">
            <xpath expr="//we-select[@data-variable='header-template']" position="inside">
                <we-button 
                    title="Scaffold"
                    data-customize-website-views=\""""+name+""".header" 
                    data-customize-website-variable="'Scaffold'" 
                    data-img="/"""+name+"""/static/src/img/wbuilder/template_wbuilder_opt.svg"
                />
            </xpath>
        </template>
        <!-- [ /TEMPLATE: HEADER OPT ]-->

        <!-- [ RECORD: HEADER ]-->
        <record id="header" model="ir.ui.view">
            <field name="name">Scaffold Header</field>
            <field name="type">qweb</field>
            <field name="key">"""+name+""".header</field>
            <field name="inherit_id" ref="website.layout"/>
            <field name="mode">extension</field>
            <field name="arch" type="xml">
                <xpath expr="//header//nav" position="replace">
                    <!-- Your custom markup here -->
                    <!-- The example below used template_header_default's markup -->
                    <t t-call="website.navbar">
                        <t t-set="_navbar_classes" t-valuef="x_wd_header d-none d-lg-block shadow-sm"/>
            
                        <div id="o_main_nav" class="container">
                            <!-- Brand -->
                            <t t-call="website.placeholder_header_brand">
                                <t t-set="_link_class" t-valuef="me-4"/>
                            </t>
                            <!-- Navbar -->
                            <t t-call="website.navbar_nav">
                                <t t-set="_nav_class" t-valuef="me-auto"/>
            
                                <!-- Menu -->
                                <t t-foreach="website.menu_id.child_id" t-as="submenu">
                                    <t t-call="website.submenu">
                                        <t t-set="item_class" t-valuef="nav-item"/>
                                        <t t-set="link_class" t-valuef="nav-link"/>
                                    </t>
                                </t>
                            </t>
                            <!-- Extra elements -->
                            <ul class="navbar-nav align-items-center gap-2 flex-shrink-0 justify-content-end ps-3">
                                <!-- Search Bar -->
                                <t t-call="website.placeholder_header_search_box">
                                    <t t-set="_layout" t-valuef="modal"/>
                                    <t t-set="_input_classes" t-valuef="border border-end-0 p-3"/>
                                    <t t-set="_submit_classes" t-valuef="border border-start-0 px-4 bg-o-color-4"/>
                                    <t t-set="_button_classes" t-valuef="o_navlink_background text-reset"/>
                                </t>
                                <!-- Text element -->
                                <t t-call="website.placeholder_header_text_element"/>
                                <!-- Social -->
                                <t t-call="website.placeholder_header_social_links"/>
                                <!-- Language Selector -->
                                <t t-call="website.placeholder_header_language_selector">
                                    <t t-set="_btn_class" t-valuef="btn-outline-secondary border-0"/>
                                    <t t-set="_txt_class" t-valuef="small"/>
                                    <t t-set="_dropdown_menu_class" t-valuef="dropdown-menu-end"/>
                                </t>
                                <!-- Sign In -->
                                <t t-call="portal.placeholder_user_sign_in">
                                    <t t-set="_link_class" t-valuef="btn btn-outline-secondary"/>
                                </t>
                                <!-- User Dropdown -->
                                <t t-call="portal.user_dropdown">
                                    <t t-set="_user_name" t-value="True"/>
                                    <t t-set="_item_class" t-valuef="dropdown"/>
                                    <t t-set="_link_class" t-valuef="btn-outline-secondary border-0 fw-bold"/>
                                    <t t-set="_user_name_class" t-valuef="small"/>
                                    <t t-set="_dropdown_menu_class" t-valuef="dropdown-menu-end"/>
                                </t>
                                <!-- Call To Action -->
                                <t t-call="website.placeholder_header_call_to_action"/>
                            </ul>
                        </div>
                    </t>
                    <t t-call="website.template_header_mobile"/>
                </xpath>
            </field>
        </record>
        <!-- [ /RECORD: HEADER ]-->

        <!-- [ CUSTOM FOOTER ]-->
        <!-- =================================== -->

        <!-- [ TEMPLATE: FOOTER OPT ]-->
        <template id="template_footer_opt" inherit_id="website.snippet_options" name="Scaffold Footer Template - Option">
            <xpath expr="//we-select[@data-variable='footer-template']" position="inside">
                <we-button title="Scaffold"
                    data-customize-website-views=\""""+name+""".footer"
                    data-customize-website-variable="'Scaffold'"
                    data-img="/"""+name+"""/static/src/img/wbuilder/template_wbuilder_opt.svg"
                />
            </xpath>
        </template>
        <!-- [ /TEMPLATE: FOOTER OPT ]-->

        <!-- [ RECORD: FOOTER ]-->
        <record id="footer" model="ir.ui.view">
            <field name="name">Scaffold Footer</field>
            <field name="type">qweb</field>
            <field name="key">"""+name+""".footer</field>
            <field name="inherit_id" ref="website.layout"/>
            <field name="mode">extension</field>
            <field name="arch" type="xml">
                <xpath expr="//div[@id='footer']" position="replace">
                    <!-- Your custom markup here -->
                    <!-- The example below used footer_custom's markup -->
                    <div id="footer" class="x_wd_footer oe_structure oe_structure_solo" t-ignore="true" t-if="not no_footer">
                        <section class="s_text_block pt40 pb16" data-snippet="s_text_block" data-name="Text">
                            <div class="container">
                                <div class="row">
                                    <div class="col-lg-2 pt24 pb24">
                                        <h5 class="mb-3">Useful Links</h5>
                                        <ul class="list-unstyled">
                                            <li><a href="/">Home</a></li>
                                            <li><a href="#">About us</a></li>
                                            <li><a href="#">Products</a></li>
                                            <li><a href="#">Services</a></li>
                                            <li><a href="#">Legal</a></li>
                                            <t t-set="configurator_footer_links" t-value="[]"/>
                                            <li t-foreach="configurator_footer_links" t-as="link">
                                                <a t-att-href="link['href']" t-esc="link['text']"/>
                                            </li>
                                            <li><a href="/contactus">Contact us</a></li>
                                        </ul>
                                    </div>
                                    <div class="col-lg-5 pt24 pb24">
                                        <h5 class="mb-3">About us</h5>
                                        <p>We are a team of passionate people whose goal is to improve everyone's life through disruptive products. We build great products to solve your business problems.
                                        <br/><br/>Our products are designed for small to medium size companies willing to optimize their performance.</p>
                                    </div>
                                    <div id="connect" class="col-lg-4 offset-lg-1 pt24 pb24">
                                        <h5 class="mb-3">Connect with us</h5>
                                        <ul class="list-unstyled">
                                            <li><i class="fa fa-comment fa-fw me-2"/><span><a href="/contactus">Contact us</a></span></li>
                                            <li><i class="fa fa-envelope fa-fw me-2"/><span><a href="mailto:info@yourcompany.example.com">info@yourcompany.example.com</a></span></li>
                                            <li><i class="fa fa-phone fa-fw me-2"/><span class="o_force_ltr"><a href="tel:+1(650)555-0111">+1 (650) 555-0111</a></span></li>
                                        </ul>
                                        <div class="s_social_media text-start o_not_editable" data-snippet="s_social_media" data-name="Social Media" contenteditable="false">
                                            <h5 class="s_social_media_title d-none" contenteditable="true">Follow us</h5>
                                            <a href="/website/social/facebook" class="s_social_media_facebook" target="_blank">
                                                <i class="fa fa-facebook rounded-circle shadow-sm o_editable_media"/>
                                            </a>
                                            <a href="/website/social/twitter" class="s_social_media_twitter" target="_blank">
                                                <i class="fa fa-twitter rounded-circle shadow-sm o_editable_media"/>
                                            </a>
                                            <a href="/website/social/linkedin" class="s_social_media_linkedin" target="_blank">
                                                <i class="fa fa-linkedin rounded-circle shadow-sm o_editable_media"/>
                                            </a>
                                            <a href="/" class="text-800">
                                                <i class="fa fa-home rounded-circle shadow-sm o_editable_media"/>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                </xpath>
            </field>
        </record>
        <!-- [ /RECORD: FOOTER ]-->
    </odoo>"""

    # Data
    zip_file.writestr(name+'/data/pages/home.xml',home)
    zip_file.writestr(name+'/data/menu.xml',menu)
    zip_file.writestr(name+'/data/images.xml',images)
    zip_file.writestr(name+'/data/presets.xml',presets)

    # Image
    zip_file.writestr(name+'/static/src/img/wbuilder/template_wbuilder_opt.svg',template_wbuilder_opt)
    zip_file.writestr(name+'/static/src/img/wbuilder/snippet_thumbnail.svg',snippet_thumbnail)
    zip_file.writestr(name+'/static/src/img/content/logo.svg',logo)

    # XML
    zip_file.writestr(name+'/static/src/xml/example.xml',xml_example)

    # Views
    zip_file.writestr(name+'/views/website_templates.xml',website_templates)
    
    img_byte_arr = BytesIO()
    im = Image.open(r'icon.png') 
    im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    zip_file.writestr(name+'/static/description/icon.png',img_byte_arr)

    img_byte_arr = BytesIO()
    im = Image.open(r'cat.gif') 
    im.save(img_byte_arr, format='GIF')
    img_byte_arr = img_byte_arr.getvalue()
    zip_file.writestr(name+'/static/src/img/content/snippets/s_wd_snippet/default.gif',img_byte_arr)

def create_scaffold():
    if len(sys.argv) < 2 :
        raise Exception("You should add the version in param like : '17.0' or '16.4'")
    if len(sys.argv) < 3 :
        raise Exception("You should add name of your module after the version number like: '17.0 my_module_name' or '16.4 my_module_name'")

    version = sys.argv[1] 
    name = sys.argv[2]
    with_python = sys.argv[3] if len(sys.argv) > 3 else False
    website_number = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    theme_number = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    zip_buffer = BytesIO()
    with ZipFile('%s.zip' % name, 'w') as zip_file:
        create_zip(zip_file, name, version, with_python, website_number, theme_number)
    zip_file.close()