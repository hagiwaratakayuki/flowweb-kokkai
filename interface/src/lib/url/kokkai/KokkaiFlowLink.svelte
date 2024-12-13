<script>
  import { keywordPretter } from "$lib/util/keyword_pretter";
  import { getKokkaiFlowUrl } from "./flow";

  export let id;
  export let keywords = [];
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
  href={getKokkaiFlowUrl(id)}
  {...props}
>
  <slot>{keywordPretter(keywords)}</slot>
</a>
