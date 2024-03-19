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
</script>

<Row class="justify-content-md-center">
  <Col sm="2" class="sticky">
    <div class="section_header">論旨の繋がり</div>
    <ul class="list-unstyled nostyle division">
      <li class="mb-2">
        <a href="#link_to" class="text-secondary" on:click={scrollLinkTo}>
          この発言に繋がる発言
        </a>
      </li>
      <li class="mb-2">
        <a href="#link_from" class="text-secondary" on:click={scrollLinkedFrom}>
          この発言から繋がる発言
        </a>
      </li>
    </ul>
  </Col>
  <Col sm="8">
    <h1>{data.title}</h1>
    <div class="bg-white mb-3">
      <h2>Data</h2>
      <Row>
        <Col sm="12" md="6">
          <dl>
            <dt>Author</dt>
            <dd>{data.author}</dd>
            <dt>Published</dt>
            <dd>{data.published}</dd>
          </dl>
        </Col>
        <Col sm="12" md="6">
          <dl>
            <dt>Keyword</dt>
            <dd>
              {#each data.keywords.slice(1, 5) as keyword}
                <span class="pe-2">{keyword}</span>
              {/each}
            </dd>
          </dl>
        </Col>
      </Row>
    </div>
    <div class="mb-5 bg-white">
      <h2>Abstract</h2>
      <p>{data.body}</p>
    </div>
    <div class="mb-5 bg-white" bind:this={linkTo} id="link_to">
      <h3 class="mb-3">This Paper Link to That Paper</h3>
      <FlatHolder overViews={data.link_to} isNextExist={false} />
    </div>
    <div class="mb-5 bg-white" bind:this={linkedFrom} id="link_from">
      <h3 class="mb-3">This Paper Linked from That Paper</h3>
      <FlatHolder
        overViews={data.linked_from}
        isNextExist={data.linked_from_next}
        bind:this={linkedFromComponent}
      />
    </div>
  </Col>
</Row>
