<script>
  import { keywordPretter } from "$lib/util/keyword_pretter";
  import BaseLink from "../BaseLink.svelte";
  import { getKokkaiFlowUrl } from "./flow";

  export let id;
  export let keywords = [];
  export let isNewWindow = true;
</script>

<BaseLink url={getKokkaiFlowUrl(id)} {isNewWindow}>
  <slot>{keywordPretter(keywords)}</slot>
</BaseLink>
