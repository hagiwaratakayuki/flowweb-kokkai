<script>
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    LineController,
  } from "chart.js";

  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    LineController,
  );
  import { TabPane } from "@sveltestrap/sveltestrap";
  import { onDestroy, beforeUpdate } from "svelte";
  export let monthStep = 20;
  export let monthCount = 12;

  let canvas;

  let frameHeight;
  let frameWidth;
  /**
   * @type {import('chart.js').Chart}
   */
  let chart;

  /**
   *
   * @param {DatasMap} datasMap
   * @param {ColorSetting} colors
   */
  export function setData(datasMap, colors = {}) {
    /**
     * @type {Object.<string, true>}
     */
    let dates = {};

    /**
     * @type {Object.<string,import("chart.js").ChartDataset>}
     */
    let datasetMap = {};

    /**
     * @type {Object.<string, Object.<string, number>>}
     */
    let scoresMap = {};

    for (const [keyword, datas] of Object.entries(datasMap)) {
      const scores = scoresMap[keyword] || {};
      for (const data of datas) {
        dates[data.datetime] = true;

        scores[data.datetime] = data.score;
      }
      scoresMap[keyword] = scores;
    }

    const datesArray = Array.from(Object.keys(dates)).sort();
    const datasetList = [];

    for (const keyword in scoresMap) {
      if (Object.hasOwnProperty.call(scoresMap, keyword)) {
        /**
         * @type {import("chart.js").ChartDataset}
         */
        const dataSet = datasetMap[keyword] || {};
        const scores = scoresMap[keyword] || {};
        const data = [];
        for (const date of datesArray) {
          const score = scores[date];
          data.push(score);
        }
        dataSet.data = data;
        if (keyword in colors) {
          const color = colors[keyword];
          if (color.backgroundColor) {
            dataSet.backgroundColor = color.backgroundColor;
          }
          if (color.borderColor) {
            dataSet.borderColor = color.borderColor;
          }
        }
        dataSet.label = keyword;
        datasetMap[keyword] = dataSet;
        datasetList.push(dataSet);
      }
    }
    if (!chart) {
      chart = new ChartJS(canvas, {
        type: "line",
        data: {
          labels: datesArray,
          datasets: datasetList,
        },
        options: {
          plugins: {
            legend: {
              display: false,
            },
          },
        },
      });
    } else {
      chart.data = {
        labels: datesArray,
        datasets: datasetList,
      };
      chart.update();
    }
  }
  beforeUpdate(function () {
    chart.update();
  });
  onDestroy(function () {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<div class=".horizontal-scroll w-100">
  <canvas bind:this={canvas} width={monthStep * monthCount} />
</div>
