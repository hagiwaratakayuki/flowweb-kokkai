<script>
  import { initSpeechUrl, getUrl } from "./speech.js";
  export let id;
  export let newWindow = true;
  let props;
  initSpeechUrl();
  $: {
    if (newWindow == true) {
      props = { target: "_brank" };
    }
  }
</script>

<a
  class="link-underline link-underline-opacity-0 link-underline-opacity-75-hover"
  href={getUrl(id)}
  {...props}
>
  <slot />
</a>
