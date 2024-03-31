<script>
  import List from "./List.svelte";
  import ComponentLayout from "../ComponentLayout.svelte";
  import { onMount } from "svelte";
  /**
   * @type {List}
   */
  let list;
  export let Hst;

  let selectedId = "test-selected";
  onMount(function () {
    if (!list) {
      return;
    }
    list.addOverviews(overviews, true);
    let selectedId = "hoge";
    setTimeout(function () {
      selectedId = "test-selected";
    }, 1500);
  });
  function onNext() {
    alert("ok");
  }
  /**
   * @type {import("$lib/ml_api/api_types/TextOverview").TextOverview[]}
   */
  const overviews = [
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test-selected",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
  ];
</script>

<ComponentLayout>
  <Hst.Story>
    <List bind:this={list} on:next={onNext} {selectedId} />
  </Hst.Story>
</ComponentLayout>
