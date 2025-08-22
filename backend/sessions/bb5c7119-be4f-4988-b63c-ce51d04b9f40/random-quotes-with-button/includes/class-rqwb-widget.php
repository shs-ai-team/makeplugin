<?php
if (!defined('ABSPATH')) {
    exit;
}

class RQWB_Widget extends WP_Widget {
    /**
     * Register widget with WordPress.
     */
    public function __construct() {
        parent::__construct(
            'rqwb_widget',
            esc_html__('Random Quotes with Button', 'random-quotes-with-button'),
            array('description' => esc_html__('Displays a random quote with a refresh button.', 'random-quotes-with-button'))
        );
    }

    /**
     * Front-end display of widget.
     *
     * @param array $args
     * @param array $instance
     */
    public function widget($args, $instance) {
        $title = '';
        if (isset($instance['title'])) {
            $title = apply_filters('widget_title', $instance['title']);
        }

        // Enqueue assets
        RQWB::get_instance()->enqueue_assets();

        echo isset($args['before_widget']) ? wp_kses_post($args['before_widget']) : '';

        if (!empty($title)) {
            // Title escaped as text
            echo (isset($args['before_title']) ? wp_kses_post($args['before_title']) : '');
            echo esc_html($title);
            echo (isset($args['after_title']) ? wp_kses_post($args['after_title']) : '');
        }

        RQWB::get_instance()->render_quote_box();

        echo isset($args['after_widget']) ? wp_kses_post($args['after_widget']) : '';
    }

    /**
     * Back-end widget form.
     *
     * @param array $instance
     * @return void
     */
    public function form($instance) {
        $title = isset($instance['title']) ? $instance['title'] : esc_html__('Random Quote', 'random-quotes-with-button');
        $field_id = $this->get_field_id('title');
        $field_name = $this->get_field_name('title');
        ?>
        <p>
            <label for="<?php echo esc_attr($field_id); ?>"><?php echo esc_html__('Title:', 'random-quotes-with-button'); ?></label>
            <input class="widefat" id="<?php echo esc_attr($field_id); ?>" name="<?php echo esc_attr($field_name); ?>" type="text" value="<?php echo esc_attr($title); ?>" />
        </p>
        <?php
    }

    /**
     * Sanitize widget form values as they are saved.
     *
     * @param array $new_instance
     * @param array $old_instance
     * @return array
     */
    public function update($new_instance, $old_instance) {
        $instance = array();
        $instance['title'] = isset($new_instance['title']) ? sanitize_text_field($new_instance['title']) : '';
        return $instance;
    }
}
