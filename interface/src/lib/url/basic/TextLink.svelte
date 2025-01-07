<script>
  import BaseLink from "../BaseLink.svelte";
  import { getTextUrl } from "./text";

  export let id;
  export let isNewWindow = false;
</script>

<BaseLink {isNewWindow} url={getTextUrl(id)}><slot /></BaseLink>
