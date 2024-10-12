<script>
  import { onMount } from "svelte";
  import { all_summary } from "$lib/ml_api/api/text/all_summary";
  import FlowWithTextList from "$lib/elements/Flow/FlowWithTextList.svelte";
  import { pushState } from "$app/navigation";

  /** @type {import('./$types').PageData} */
  export let data;

  /**
   * @type {FlowWithTextList}
   */
  let flowWithTextList;
  onMount(async function () {
    flowWithTextList.setInitData(data);

    //flowWithTextList.initError();
  });
</script>

<FlowWithTextList bind:this={flowWithTextList} />
