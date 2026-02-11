<script>
  import BaseLink from "../BaseLink.svelte";
  import { getMeetingUrl } from "./meeting";

  export let id;
  export let isNewWindow = false;
</script>

<BaseLink {isNewWindow} url={getMeetingUrl(id)}><slot /></BaseLink>
