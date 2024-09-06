<h3 id="drcodecover">drcodecover</h3>
<p><strong>drcodecover</strong> is a Python package that provides a wrapper around Sentry, making it easy to configure and use Sentry&#39;s features, including profiling and error handling.</p>
<h2 id="installation">Installation</h2>
<p>To install the package, run:</p>
<p>bash</p>
<h2 id="copy-code--pip-install-drcodecover--getting-started">Copy code
<pre><code class="language-const"> pip install drcodecover
</code></pre>
Getting Started</h2>
<p><strong>Basic Usage</strong></p>
<p>python</p>
<p>Copy code</p>
<pre><code class="language-const"> 
from drcodecover import init_drcode
config = {
'public_key': 'yourPublicKey',
'project_id': 'yourProjectId',
'traces_sample_rate': 1.0, # optional
'profiles_sample_rate': 1.0 # optional
}
init_drcode(config)

</code></pre></p>

<h2 id="configuration">Configuration</h2>
<p><strong>Configuration Object</strong></p>
<ul>
<li><code>public_key</code> (str): The public key for Sentry.</li>
<li><code>project_id</code> (str): The Sentry project ID.</li>
<li><code>traces_sample_rate</code> (float, optional): The sample rate for tracing (default: 1.0).</li>
<li><code>profiles_sample_rate</code> (float, optional): The sample rate for profiling (default: 1.0).</li>
</ul>
<h2 id="api-reference">API Reference</h2>
<p><strong>Functions</strong></p>
<ul>
<li><p><strong>init_drcode(config: dict) -&gt; None</strong></p>
<p>Initializes Sentry with the provided configuration.</p>
<ul>
<li><strong>config</strong> (dict): The configuration dictionary.</li>
</ul>
</li>
</ul>
<p><strong>Configuration Dictionary</strong></p>
<p>The configuration dictionary should contain the following keys:</p>
<ul>
<li><code>public_key</code> (str): The public key for Sentry.</li>
<li><code>project_id</code> (str): The Sentry project ID.</li>
<li><code>traces_sample_rate</code> (float, optional): The sample rate for tracing (default: 1.0).</li>
<li><code>profiles_sample_rate</code> (float, optional): The sample rate for profiling (default: 1.0).</li>
</ul>
<h2 id="license">License</h2>
<p>This project is licensed under the MIT License.</p>
<h2 id="version">Version</h2>
<p>1.0.2</p>
