/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run "npm run dev" in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run "npm run deploy" to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    console.log(`Received request for: ${url.pathname} with query: ${url.search}`);
    try {
      // Check if the request path starts with '/.well-known/webfinger'
      if (url.pathname.startsWith('/.well-known/webfinger')) {
        const resource = url.searchParams.get('resource');
        // Check if the resource parameter is present and starts with 'acct:'
        if (resource && resource.startsWith('acct:')) {
          const email = resource.substring(5); // Extract the email part
          const issuerUrl = 'https://authentik.cloudydad.world/application/o/tailscale/';
          // Construct the response data
          const responseData = {
            subject: resource,
            links: [
              {
                rel: 'http://openid.net/specs/connect/1.0/issuer',
                href: issuerUrl,
              },
              {
                rel: 'authorization_endpoint',
                href: issuerUrl + 'oauth2/authorize',
              },
              {
                rel: 'token_endpoint',
                href: issuerUrl + 'oauth2/token',
              },
              {
                rel: 'userinfo_endpoint',
                href: issuerUrl + 'userinfo',
              },
              {
                rel: 'jwks_uri',
                href: issuerUrl + 'jwks',
              },
            ],
          };
          // Return the JSON response
          return new Response(JSON.stringify(responseData), {
            headers: { 'Content-Type': 'application/json' },
            status: 200,
          });
        } else {
          console.warn(`Invalid resource parameter: ${resource}`);
          return new Response('Invalid resource parameter.', { status: 400 });
        }
      } else {
        console.warn(`Invalid path: ${url.pathname}`);
        return new Response('Invalid path.', { status: 404 });
      }
    } catch (error) {
      console.error('Error processing request:', error);
      return new Response('Internal Server Error', { status: 500 });
    }
  },
};
