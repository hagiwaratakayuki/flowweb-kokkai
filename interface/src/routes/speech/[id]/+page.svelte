<script>
  import { Row, Col, Button } from "@sveltestrap/sveltestrap";
  import FlatHolder from "$lib/elements/TextOverview/FlatHolder.svelte";

  /** @type {import('./$types').PageData} */
  export let data;

  /**
   * @type {HTMLElement}
   */
  let linkTo;
  /**
   * @type {HTMLElement}
   */
  let linkedFrom;
  /**
   * @type {FlatHolder}
   */
  let linkedFromComponent;
  function scrollLinkTo() {
    linkTo.scrollIntoView({ behavior: "smooth" });
  }
  function scrollLinkedFrom() {
    linkedFrom.scrollIntoView({ behavior: "smooth" });
  }
  /**
   *
   * @param {string} text
   */
  function splitbr(text) {
    return text.split(/(\r|\n|\r\n)/);
  }
</script>

<Row class="justify-content-md-center">
  <Col sm="2" class="sticky">
    <h2 class="section_header">質疑</h2>
    <div class="bg-white">
      <ul class="list-group">
        {#each data.discussion as discussion}
          <li
            class="list-group-item"
            class:active={discussion.id === data.speech.id}
            aria-current={discussion.id === data.speech.id}
          >
            {discussion.title}
          </li>
        {/each}
      </ul>
    </div>
  </Col>
  <Col sm="8">
    <h2 class="section_header">発言</h2>
    <p class="bg-white mb-3 p-3">
      {#each splitbr(data.speech.body) as line}
        {line}<br />
      {/each}
    </p>
    <div class="bg-white mb-3 p-3">
      <dl>
        <dt>発言者</dt>
        <dd>{data.speech.speaker}</dd>
        <dt>委員会</dt>
        <dd>{data.speech.house} {data.speech.meeting}</dd>
        <dt>回次</dt>
        <dd>第{data.speech.session}回国会</dd>
        <dt>号数</dt>
        <dd>{data.speech.issue}</dd>
      </dl>
      <p>
        <a href={data.speech.url} target="_blank">この発言を会議録で見る</a>
      </p>
    </div>
  </Col>
</Row>
