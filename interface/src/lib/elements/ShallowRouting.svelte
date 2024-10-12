<script>
  import { createEventDispatcher } from "svelte";
  import { pushState } from "$app/navigation";
  import { page, updated } from "$app/stores";
  const dispatch = createEventDispatcher();

  $: if ($updated === true) {
    dispatch("update", $page.state);
  }

  export function moveTo(url, params) {
    pushState(url, params);
  }
</script>
