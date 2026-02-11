<script>
  import { Row, Col } from "@sveltestrap/sveltestrap";
  export let sideClass = "";
  export let mainClass = "";
</script>

<Row class="justify-content-md-center">
  <Col xs="12" sm="4" md="2" class={sideClass}>
    <slot name="side"></slot>
  </Col>
  <Col xs="12" sm="8" md="10" class={mainClass}>
    <slot name="main"></slot>
  </Col>
</Row>
