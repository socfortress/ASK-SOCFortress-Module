[<img src="images/logo_orange.svg" align="right" width="100" height="100" />](https://www.socfortress.co/)

# SOCFortress Knowledge Base Integration [![Awesome](https://img.shields.io/badge/SOCFortress-Worlds%20First%20Free%20Cloud%20SOC-orange)](https://www.socfortress.co/trial.html)
> Integrate your `Wazuh-Manager` or `Graylog` with the SOCFortress KnowlegeBase API to receive real-time recommend actions regarding SIGMA rule detection.


[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![your-own-soc-free-for-life-tier](https://img.shields.io/badge/Get%20Started-Demo%20Walkthrough-orange)](https://youtu.be/2EMb6zYx7_E)

<!-- PROJECT LOGO -->
<br />
<div align="center" width="50" height="50">
  <a href="https://www.socfortress.co/">
    <img src="images/logo_purple_resize.png" alt="Logo">
  </a>

  <h3 align="center">SOCFortress Knowledge Base API</h3>

  <p align="center">
    Integrate your Wazuh-Manager or Graylog with the SOCFortress KnowlegeBase API to receive real-time recommend actions regarding SIGMA rule detection.
    <br />
    <a href="https://www.socfortress.co/request_beta.html"><strong>Register for API Key »</strong></a>
    <br />
    <br />
    <a href="https://paypal.me/socfortress?country.x=US&locale.x=en_US"><strong>💰 Make a Donation »</strong></a>
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#knowledge-base-api">Knowledge Base API</a>
    </li>
    <li>
      <a href="#wazuh-manager-integration">Wazuh-Manager Integration</a>
    </li>
    <li>
    <a href="#graylog-integration">Graylog Integration</a>
    </li>
  </ol>
</details>



<!-- Knowledge Base API -->
# Knowledge Base API
> The SOCFortress Knowledge Base API helps to provide some context and recommended actions to your security alerts. The integration supports both `Wazuh-Manager` and `Graylog`. 

## API-KEY
> The API key is required to authenticate with the API. To obtain an API key, please fill out a request form at [SOCFortress.co](https://www.socfortress.co/request_beta.html).

## Criteria
> The API is currently **only** built for the following criteria:
* `Windows Chainsaw Events` - Follow our [Wazuh and Chainsaw integration for near real time SIGMA detection](https://medium.com/@socfortress/wazuh-and-chainsaw-integration-for-near-real-time-sigma-detection-6f3e729e892) to integrate Chainsaw with your Windows endpoints.
* `SOCFortress Wazuh Detection Rules` - Follow our [Wazuh Rules Install Guide](https://github.com/socfortress/Wazuh-Rules) to integrate SOCFortress's Wazuh detection rules with your Wazuh-Manager.
* `Valid API Key` - Request via [our website](https://www.socfortress.co/request_beta.html).

> ⚠ **NOTE:** API quotas are currently restricted to `100` requests per day. The API is currently in beta and is subject to change. Please contact us at [helpdesk.socfortress.co](https://servicedesk.socfortress.co/help/2979687893) if you have any questions or concerns.

* `SOCFortress API Wazuh Rules` - [200980-socfortress.xml](https://raw.githubusercontent.com/socfortress/Wazuh-Rules/main/SOCFortress%20API/200980-socfortress.xml) - **NOT REQUIRED IF INTEGRATING WITH GRAYLOG**

<!-- Wazuh-Manager Integration -->
# Wazuh-Manager Integration
**Not Recommended - Use Graylog Instead If You Can - Graylog's built in Caching will save your API quota**
> Follow the steps below to integrate the SOCFortress Knowledge Base API with your Wazuh-Manager. **NOT REQUIRED IF INTEGRATING WITH GRAYLOG**
1. Download the `custom-asksocfortress.py` file from the GitHub repository and copy it to `/var/ossec/integrations` of your `Wazuh-Manager`.

```
# Download the custom-asksocfortress.py file from the GitHub repository
curl -o custom-asksocfortress.py https://raw.githubusercontent.com/socfortress/ASK-SOCFortress-Module/main/custom-asksocfortress.py

# Copy the custom-asksocfortress.py file to /var/ossec/integrations
sudo cp custom-asksocfortress.py /var/ossec/integrations

# Change ownership to root:wazuh
sudo chown root:wazuh /var/ossec/integrations/custom-asksocfortress.py

# Set permissions to -rwxr-x---
sudo chmod 750 /var/ossec/integrations/custom-asksocfortress.py

# Clean up the downloaded file
rm custom-asksocfortress.py
```

2. Edit the `/var/ossec/etc/ossec.conf` file and add the following lines to the `ossec.conf` file.

```
<integration>
    <name>custom-asksocfortress.py</name>
    <api_key>YOUR_API_KEY</api_key>
    <group>chainsaw</group>
    <alert_format>json</alert_format>
 </integration>
```
> ⚠ **NOTE:** The `group` parameter is the name of the Wazuh rule groups that you want to integrate with the SOCFortress Knowledge Base API. All of the below rule groups are supported: 
* `chainsaw`


> The `alert_format` parameter is the format of the alert that you want to receive from the SOCFortress Knowledge Base API. The `api_key` parameter is the API key that you received from SOCFortress.

3. Restart the Wazuh-Manager service.

```
sudo systemctl restart wazuh-manager
```

4. If you have any issues, set the `integrator_debug` to `2` in the `/var/ossec/etc/local_internal_options.conf` file and restart the Wazuh-Manager service.

    * Tail the `ossec.log` file and ensure you see valid responses from the SOCFortress Knowledge Base API. `tail -f /var/ossec/logs/ossec.log | grep socfortress`

<div align="center" width="50" height="50">
  <a href="https://raw.githubusercontent.com/socfortress/ASK-SOCFortress-Module/main/images/ossec_log.PNG">
    <img src="images/ossec_log.PNG" alt="Logo">
  </a>

  <h3 align="center">Ossec.log File</h3>
  </p>
</div>

If working correctly, rule id `200986` will trigger when a positive IoC is found.

<div align="center" width="50" height="50">
  <a href="https://github.com/socfortress/SOCFortress-Threat-Intel/images/wazuh_hits.PNG">
    <img src="images/wazuh_hits.PNG" alt="Logo">
  </a>

  <h3 align="center">SOCFortress Knowledge Base Fields</h3>
  </p>
</div>



<!-- Graylog Integration -->
# Graylog Integration
> Follow the steps below to integrate the SOCFortress Knowledge Base API with your Graylog instance.
1. Create `ASK SOCFortress - Windows` Data Adapter.
* `Title` - ASK SOCFortress - Windows
* `Description` - ASK SOCFortress for Windows SIGMA
* `Name` - ask-socfortress-windows
* `Lookup URL` - https://api.socfortress.co/v1/sigma?name=${key}
* `Single value JSONPath` - $.message
* `HTTP Headers`-
    * `Content-Type` - application/json
    * `module-version` - 1.0
    * `product` - windows
    * `x-api-key` - YOUR_API_KEY

> ⚠ **NOTE:** Verify connection to the SOCFortress Knowledge Base API. Use Value `Suspicious%20Program%20Location%20with%20Network%20Connections` to test.

<div align="center" width="50" height="50">
  <a href="https://github.com/socfortress/ASK-SOCFortress-Module/images/graylog_response.png">
    <img src="images/graylog_response.PNG" alt="Logo">
  </a>

  <h3 align="center">Graylog Response</h3>
  </p>
</div>

2. Create `ASK SOCFortress - Windows` Cache.
* `Cache Type` - Node-local, in-memory cache
* `Title` - ASK SOCFortress - Windows
* `Description` - ASK SOCFortress - Windows
* `Name` - ask-socfortress-windows
* `Maximum Entries` - 1000
* `Expire after access` - 5 minutes

3. Create `ASK SOCFortress - Windows` Lookup Table.
* `Title` - ASK SOCFortress - Windows
* `Description` - ASK SOCFortress - Windows
* `Name` - ask_socfortress_windows
* `Data Adapter` - ASK SOCFortress - Windows (ask-socfortress-windows)
* `Cache` - ASK SOCFortress - Windows (ask-socfortress-windows)

4. Create Pipeline Rules to first encode the `data_name` field and then lookup the encoded `data_name` field in the `ASK SOCFortress - Windows` Lookup Table.
    1. URL Encode `data_name` field for ASK SOCFortress API
    ```
    rule "URL Encode data_name field for ASK SOCFortress API"
    when
        has_field("data_name") AND $message.rule_group2 == "chainsaw" AND $message.data_logsource_product == "windows"
    then
        let replaced = replace(to_string($message.data_name), " ", "%20");
        set_field("sigma_name_encoded", replaced);
    end
    ```
    2. ASK SOCFORTRESS WINDOWS - CHAINSAW
    ```
    rule "ASK SOCFORTRESS WINDOWS - CHAINSAW"
    when
        has_field("sigma_name_encoded")
    then
        let ask_socfortress = to_string($message.sigma_name_encoded);
        let ldata = lookup_value("ask_socfortress_windows", ask_socfortress);
        set_field("ask_socfortress_message", ldata);
    end
    ```


<br />

<!-- CONTACT -->
# Contact

SOCFortress - [![LinkedIn][linkedin-shield]][linkedin-url] - info@socfortress.co

<div align="center">
  <h2 align="center">Let SOCFortress Take Your Open Source SIEM to the Next Level</h3>
  <a href="https://www.socfortress.co/contact_form.html">
    <img src="images/Email%20Banner.png" alt="Banner">
  </a>


</div>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/socfortress/Wazuh-Rules
[contributors-url]: https://github.com/socfortress/Wazuh-Rules/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/socfortress/Wazuh-Rules
[forks-url]: https://github.com/socfortress/Wazuh-Rules/network/members
[stars-shield]: https://img.shields.io/github/stars/socfortress/Wazuh-Rules
[stars-url]: https://github.com/socfortress/Wazuh-Rules/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/badge/Help%20Desk-Help%20Desk-blue
[license-url]: https://servicedesk.socfortress.co/help/2979687893
[linkedin-shield]: https://img.shields.io/badge/Visit%20Us-www.socfortress.co-orange
[linkedin-url]: https://www.socfortress.co/
