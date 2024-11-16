<script>
  import FlowWithTextList from "./FlowWithTextList.svelte";
  import Layout from "../ComponentLayout.svelte";
  import { onMount } from "svelte";
  import { all_summary } from "$lib/ml_api/api/node/all_summary";
  import Flow from "./Flow.svelte";
  export let Hst;
  /**
   * @type {FlowWithTextList}
   */
  let flowWithTextList;
  //@todo change to mockdata;
  onMount(async function () {
    const textOverview = await all_summary();
    flowWithTextList.setInitData(textOverview);
  });
</script>

<Hst.Story>
  <Layout>
    <FlowWithTextList bind:this={flowWithTextList} />
  </Layout>
</Hst.Story>
