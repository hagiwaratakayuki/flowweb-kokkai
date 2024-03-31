<script>
  import { onMount } from "svelte";
  import { all_summary } from "$lib/ml_api/api/text/all_summary";
  import FlowWithTextList from "$lib/elements/FlowWithTextList.svelte";

  /**
   * @type {FlowWithTextList}
   */
  let flowWithTextList;
  onMount(async function () {
    try {
      /**
       * @typedef {import("$lib/ml_api/api_types/TextOverview").TextOverview} TextOverview
       * @type {Array<TextOverview>}
       */
      const overViews = await all_summary();
      flowWithTextList.setInitData(overViews);
    } catch (error) {
      flowWithTextList.initError();
    }
  });
</script>

<FlowWithTextList bind:this={flowWithTextList} />
