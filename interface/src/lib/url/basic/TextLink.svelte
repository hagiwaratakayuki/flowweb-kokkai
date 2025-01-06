<script>
  import BaseLink from "../BaseLink.svelte";
  import { getTextUrl } from "./text";

  export let id;
  export let newWindow = false;
</script>

<BaseLink {newWindow} url={getTextUrl(id)}><slot /></BaseLink>
