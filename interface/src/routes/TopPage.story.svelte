<script>
  import TopPage from "./+page.svelte";
  import ComponentLayout from "$lib/elements/ComponentLayout.svelte";
  export let Hst;

  /**
   * @type {import("$lib/ml_api/api_types/TextOverViews").TextOverviews}
   */
  const data = {
    texts: [
      {
        id: 1,
        title: "テスト発言",
        author: "テスト議員",
        y: 0.5,
        published: "1990/01/01",
        weight: 1,
        link_to: [2],
      },
      {
        title: "テスト発言2",
        author: "テスト議員1",
        id: 2,
        y: -0.7,
        published: "1990/01/10",
        weight: 0.5,
      },
    ],
    cursor: "",
  };
</script>

<Hst.Story>
  <ComponentLayout>
    <TopPage {data} />
  </ComponentLayout>
</Hst.Story>
