<script>
  import Card from "./Card.svelte";
  import ComponentLayout from "../ComponentLayout.svelte";
  export let Hst;
  /**
   * @type {import("$lib/ml_api/api_types/TextOverview").TextOverview}
   */
  const overview = {
    id: "test",
    body: "loren epsum but efront number",
    author: "fooo hoge fuga",
    published: new Date().toDateString(),
  };
</script>

<ComponentLayout>
  <Hst.Story>
    <Card {overview} />
  </Hst.Story>
</ComponentLayout>
