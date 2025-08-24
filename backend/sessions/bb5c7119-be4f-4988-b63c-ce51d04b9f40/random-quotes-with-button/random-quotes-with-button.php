<?php
/**
 * Plugin Name: Random Quotes with Button
 * Description: Display a random quote with a refresh button
 * Version: 1.0.0
 * Author: makeplugin
 * Text Domain: random-quotes-with-button
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) {
    exit;
}

if (!defined('RQWB_VERSION')) {
    define('RQWB_VERSION', '1.0.0');
}

if (!defined('RQWB_PLUGIN_FILE')) {
    define('RQWB_PLUGIN_FILE', __FILE__);
}

if (!defined('RQWB_PLUGIN_DIR')) {
    define('RQWB_PLUGIN_DIR', plugin_dir_path(__FILE__));
}

if (!defined('RQWB_PLUGIN_URL')) {
    define('RQWB_PLUGIN_URL', plugin_dir_url(__FILE__));
}

/**
 * Load text domain
 */
function rqwb_load_textdomain() {
    load_plugin_textdomain('random-quotes-with-button', false, dirname(plugin_basename(__FILE__)) . '/languages');
}
add_action('plugins_loaded', 'rqwb_load_textdomain');

// Includes
require_once RQWB_PLUGIN_DIR . 'includes/class-rqwb.php';
require_once RQWB_PLUGIN_DIR . 'includes/class-rqwb-widget.php';

/**
 * Initialize plugin
 */
function rqwb_init_plugin() {
    $instance = RQWB::get_instance();
    $instance->init();
}
add_action('init', 'rqwb_init_plugin');

/**
 * Register widget
 */
function rqwb_register_widget() {
    register_widget('RQWB_Widget');
}
add_action('widgets_init', 'rqwb_register_widget');
