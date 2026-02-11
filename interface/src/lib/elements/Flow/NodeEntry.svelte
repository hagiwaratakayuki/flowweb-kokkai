<script>
  import { createEventDispatcher } from "svelte";

  const dispatcher = createEventDispatcher();
  /**
   * @type {import("$lib/relay_types/flow").FlowEntry}
   */
  export let entry;
  export let selectedId;
  let element;
  let isSelected = false;
  $: {
    isSelected = selectedId === entry;
  }
  function onMouseOver() {
    isSelected = true;
    dispatcher("activate", entry.id);
  }
  function onMouseOut() {
    dispatcher("deactivate", entry.id);
  }
</script>

<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<li
  class="list-group-item border-start-0 border-end-0"
  bind:this={element}
  on:mouseover={onMouseOver}
  on:mouseout={onMouseOut}
>
  <a href="/text/{entry.id}" class:selected={isSelected}>
    {entry.title.slice(0, 15)}...
  </a>
</li>
