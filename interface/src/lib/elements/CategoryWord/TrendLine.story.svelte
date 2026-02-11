<script>
  import TrendLine from "./TrendLine.svelte";
  import { onMount } from "svelte";
  export let Hst;
  /**
   * @type {TrendLine}
   */
  let trendLine;
  onMount(function () {
    if (!trendLine) {
      return;
    }
    console.log(trendLine);
    trendLine.setData(
      {
        test1: [
          {
            datetime: "2019/07",
            score: 0.2,
          },
          {
            datetime: "2019/08",
            score: 0.3,
          },
          {
            datetime: "2019/09",
            score: 0.4,
          },
        ],
      },
      {
        test1: {
          backgroundColor: "#ff0000",
          borderColor: "#ff0000",
        },
      }
    );
  });
</script>

<Hst.Story>
  <div style="width: 100%; height:300px;">
    <TrendLine bind:this={trendLine} />
  </div>
</Hst.Story>
