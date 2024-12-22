<script>
  import BaseLink from "../BaseLink.svelte";
  import { getSpeakerUrl } from "./speaker";

  export let id;
  export let newWindow = false;
</script>

<BaseLink {newWindow} url={getSpeakerUrl(id)}><slot /></BaseLink>
