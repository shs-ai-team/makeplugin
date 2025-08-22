<?php
if (!defined('ABSPATH')) {
    exit;
}

class RQWB {
    /**
     * Singleton instance
     *
     * @var RQWB
     */
    private static $instance = null;

    /**
     * Get instance
     *
     * @return RQWB
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Init hooks
     */
    public function init() {
        add_shortcode('random_quotes_with_button', array($this, 'shortcode_handler'));
        add_action('wp_enqueue_scripts', array($this, 'register_assets'));
    }

    /**
     * Register scripts and styles
     */
    public function register_assets() {
        wp_register_style(
            'rqwb-style',
            RQWB_PLUGIN_URL . 'assets/css/style.css',
            array(),
            RQWB_VERSION
        );

        wp_register_script(
            'rqwb-script',
            RQWB_PLUGIN_URL . 'assets/js/rqwb.js',
            array('wp-i18n'),
            RQWB_VERSION,
            true
        );

        // Localize quotes and strings
        $data = array(
            'quotes' => $this->get_quotes_for_js(),
            'i18n'   => array(
                'newQuote'   => esc_html__('New Quote', 'random-quotes-with-button'),
                'buttonAria' => esc_attr__('Get a new random quote', 'random-quotes-with-button'),
            ),
        );

        wp_localize_script('rqwb-script', 'rqwbData', $data);
    }

    /**
     * Enqueue assets (called when rendering)
     */
    public function enqueue_assets() {
        wp_enqueue_style('rqwb-style');
        wp_enqueue_script('rqwb-script');
    }

    /**
     * Shortcode handler
     *
     * @param array $atts
     * @return string
     */
    public function shortcode_handler($atts) {
        $atts = shortcode_atts(
            array(
                'class' => '',
            ),
            $atts,
            'random_quotes_with_button'
        );

        $this->enqueue_assets();

        ob_start();
        $this->render_quote_box($atts);
        return ob_get_clean();
    }

    /**
     * Render the quote box template
     *
     * @param array $args
     * @param array $instance Optional widget instance for context
     */
    public function render_quote_box($args = array(), $instance = array()) {
        $args = is_array($args) ? $args : array();
        $class = '';
        if (!empty($args['class'])) {
            $class = sanitize_html_class($args['class']);
        }

        $quotes = $this->get_quotes();
        $initial_index = $this->get_random_index(count($quotes));
        $quote = $quotes[$initial_index];

        $container_id = 'rqwb-' . wp_generate_uuid4();

        $data = array(
            'id'            => $container_id,
            'class'         => $class,
            'initial_index' => (int) $initial_index,
            'text'          => $quote['text'],
            'author'        => $quote['author'],
        );

        // Include template
        $template = RQWB_PLUGIN_DIR . 'templates/quote-box.php';
        if (file_exists($template)) {
            /** @psalm-suppress UnresolvableInclude */
            include $template;
        }
    }

    /**
     * Get random index helper
     *
     * @param int $max
     * @return int
     */
    private function get_random_index($max) {
        if ($max <= 1) {
            return 0;
        }
        return wp_rand(0, $max - 1);
    }

    /**
     * Get quotes for JS (sanitized for output to front-end)
     *
     * @return array
     */
    private function get_quotes_for_js() {
        $out = array();
        foreach ($this->get_quotes() as $q) {
            $out[] = array(
                'text'   => $q['text'],
                'author' => $q['author'],
            );
        }
        return $out;
    }

    /**
     * Quotes list
     *
     * @return array
     */
    private function get_quotes() {
        // Translators: These are example quotes displayed by the plugin.
        return array(
            array(
                'text'   => esc_html__('The only limit to our realization of tomorrow is our doubts of today.', 'random-quotes-with-button'),
                'author' => esc_html__('Franklin D. Roosevelt', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('In the middle of difficulty lies opportunity.', 'random-quotes-with-button'),
                'author' => esc_html__('Albert Einstein', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('Do what you can, with what you have, where you are.', 'random-quotes-with-button'),
                'author' => esc_html__('Theodore Roosevelt', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('It always seems impossible until it’s done.', 'random-quotes-with-button'),
                'author' => esc_html__('Nelson Mandela', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('Simplicity is the ultimate sophistication.', 'random-quotes-with-button'),
                'author' => esc_html__('Leonardo da Vinci', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('Well begun is half done.', 'random-quotes-with-button'),
                'author' => esc_html__('Aristotle', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('Success is not final, failure is not fatal: it is the courage to continue that counts.', 'random-quotes-with-button'),
                'author' => esc_html__('Winston Churchill', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('If you want to go fast, go alone. If you want to go far, go together.', 'random-quotes-with-button'),
                'author' => esc_html__('African Proverb', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('The best way to predict the future is to create it.', 'random-quotes-with-button'),
                'author' => esc_html__('Peter Drucker', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('We are what we repeatedly do. Excellence, then, is not an act, but a habit.', 'random-quotes-with-button'),
                'author' => esc_html__('Will Durant', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('Happiness is not something ready made. It comes from your own actions.', 'random-quotes-with-button'),
                'author' => esc_html__('Dalai Lama', 'random-quotes-with-button'),
            ),
            array(
                'text'   => esc_html__('Act as if what you do makes a difference. It does.', 'random-quotes-with-button'),
                'author' => esc_html__('William James', 'random-quotes-with-button'),
            ),
        );
    }
}
