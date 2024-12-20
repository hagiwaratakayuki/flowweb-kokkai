<script>
  import BaseLink from "../BaseLink.svelte";
  import { getMeetingUrl } from "./meeting";

  export let id;
  export let newWindow = false;
</script>

<BaseLink {newWindow} url={getMeetingUrl(id)}><slot /></BaseLink>
