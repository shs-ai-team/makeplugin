<?php
if (!defined('ABSPATH')) {
    exit;
}
/** @var array $data */
$container_id = isset($data['id']) ? $data['id'] : 'rqwb-' . wp_generate_uuid4();
$container_class = 'rqwb-quote-box';
if (!empty($data['class'])) {
    $container_class .= ' ' . sanitize_html_class($data['class']);
}
$initial_index = isset($data['initial_index']) ? (int) $data['initial_index'] : 0;
$text = isset($data['text']) ? $data['text'] : '';
$author = isset($data['author']) ? $data['author'] : '';
?>
<div id="<?php echo esc_attr($container_id); ?>" class="<?php echo esc_attr($container_class); ?>" data-rqwb-index="<?php echo esc_attr((string) $initial_index); ?>" role="region" aria-live="polite">
    <blockquote class="rqwb-quote">
        <span class="rqwb-quote-text"><?php echo esc_html($text); ?></span>
        <?php if (!empty($author)) : ?>
            <cite class="rqwb-quote-author">&mdash; <?php echo esc_html($author); ?></cite>
        <?php endif; ?>
    </blockquote>
    <button type="button" class="rqwb-button" aria-label="<?php echo esc_attr__( 'Get a new random quote', 'random-quotes-with-button' ); ?>">
        <?php echo esc_html__( 'New Quote', 'random-quotes-with-button' ); ?>
    </button>
</div>
