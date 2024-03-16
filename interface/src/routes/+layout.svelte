<script>
  import { Container } from "@sveltestrap/sveltestrap";
  import "bootstrap/dist/css/bootstrap.css";
  import "./app.css";
</script>

<Container fluid={true} id="container">
  <slot />
</Container>
