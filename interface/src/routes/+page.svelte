<script>
  import { onMount } from "svelte";
  import { all_summary } from "$lib/ml_api/api/node/all_summary";
  import FlowWithTextList from "$lib/elements/Kokkai/Flow.svelte";
  import { pushState } from "$app/navigation";
  import { page } from "$app/stores";
  import { getData } from "$lib/shallowrouting/funcs";
  import HtmlHeader from "$lib/elements/HtmlHeader.svelte";
  /** @type {import('./$types').PageData} */
  export let data;

  /** @type {import('./$types').PageData} */

  /* let _data;
  $: {
    _data = getData($page.state, data);
    
  }*/
</script>

<HtmlHeader></HtmlHeader>
<h1 class="w-100 text-center mb-5">Thought Flow 国会編</h1>
<h2 class="mb-3 section_header">最近の主な議論</h2>
<FlowWithTextList data={data.summary} />
