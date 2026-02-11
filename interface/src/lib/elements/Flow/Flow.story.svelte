<script>
  import Flow from "./Flow.svelte";
  export let Hst;
  const nodes = [
    {
      id: 1,
      y: 0.5,
      published: "1990/01/01",
      weight: 1,
    },
    {
      id: 2,
      y: -0.7,
      published: "1990/01/10",
      weight: 0.5,
    },
  ];
  const edges = [
    {
      from: 1,
      to: 2,
    },
  ];

  const flow = {
    nodes,
    edges,
  };
</script>

<Hst.Story>
  <div style="width: 100%; height:300px;">
    <Flow {flow} />
  </div>
</Hst.Story>
