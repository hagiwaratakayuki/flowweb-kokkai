<script>
  export let url;
  export let newWindow = true;
  let props;

  $: {
    if (newWindow == true) {
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
