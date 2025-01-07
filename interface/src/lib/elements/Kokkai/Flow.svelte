<script>
  import { getSpeechUrl } from "$lib/url/kokkai/speech";
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

<FlowWithTextList bind:this={flowWithTextList} getItemUrl={getSpeechUrl}>
  <div slot="sidebar"><slot name="sidebar" /></div>
  <div slot="main"><slot name="main" /></div>
</FlowWithTextList>
