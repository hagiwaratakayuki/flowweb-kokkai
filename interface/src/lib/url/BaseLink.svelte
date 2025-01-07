<script>
  export let url;
  export let isNewWindow = true;
  let props;

  $: {
    if (isNewWindow == true) {
      props = { target: "_brank" };
    }
  }
</script>

<a
  class="link-underline link-underline-opacity-0 link-underline-opacity-75-hover"
  href={url}
  {...props}
>
  <slot />
</a>
