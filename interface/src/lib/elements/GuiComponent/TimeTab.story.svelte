<script>
  import TimeTab from "./TimeTab.svelte";
  export let Hst;
</script>

<Hst.Story>
  <TimeTab>
    <div slot="controll">controll</div>
    <div slot="flow">flow</div>
    <div slot="categryword">categoryword</div>
  </TimeTab>
</Hst.Story>
