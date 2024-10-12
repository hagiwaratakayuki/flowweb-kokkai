<script>
  import FlowWithTextList from "../Flow/FlowWithTextList.svelte";
  /**
   * @type {FlowWithTextList}
   */
  let flowWithTextList;
  export function setData(data) {
    flowWithTextList.setInitData(data);
  }
</script>

<slot></slot>
<FlowWithTextList bind:this={flowWithTextList}></FlowWithTextList>
