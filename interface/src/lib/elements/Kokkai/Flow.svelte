<script>
  import FlowWithTextList from "../Flow/FlowWithTextList.svelte";

  import { onMount } from "svelte";
  export let data;
  let _isMounted = false;

  onMount(function () {
    _isMounted = true;
  });

  /**
   * @type {FlowWithTextList}
   */
  let flowWithTextList;
  $: if (_isMounted === true) {
    flowWithTextList.setInitData(data);
  }
</script>

{#if $$slots.controll}
  <div class="division">
    <slot name="controll"></slot>
  </div>
{/if}
<FlowWithTextList bind:this={flowWithTextList}></FlowWithTextList>
