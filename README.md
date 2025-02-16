# [! important] The AgentConnect repository has been moved to a new address【仓库已迁移☞】: 

[https://github.com/agent-network-protocol/AgentConnect](https://github.com/agent-network-protocol/AgentConnect)

<div align="center">
  
[English](README.md) | [中文](README.cn.md)

</div>

## AgentConnect

### What is AgentConnect

AgentConnect is an open-source implementation of the [Agent Network Protocol (ANP)](https://github.com/chgaowei/AgentNetworkProtocol).

The Agent Network Protocol (ANP) aims to become **the HTTP of the Agentic Internet era**.

Our vision is to **define how agents connect with each other and build an open, secure, and efficient collaboration network for billions of agents**.

<p align="center">
  <img src="/images/agentic-web.png" width="50%" alt="Agentic Web"/>
</p>

While current internet infrastructure is well-established, there's still a lack of optimal communication and connection solutions for the specific needs of agent networks. We are committed to addressing three major challenges faced by agent networks:

- 🌐 **Interconnectivity**: Enable communication between all agents, break down data silos, and allow AI to access complete contextual information.
- 🖥️ **Native Interfaces**: AI shouldn't have to mimic human internet interactions; it should interact with the digital world through its most proficient methods (APIs or communication protocols).
- 🤝 **Efficient Collaboration**: Leverage AI for self-organizing and self-negotiating agents to build a more cost-effective and efficient collaboration network than the existing internet.

### AgentConnect Architecture

The technical architecture of AgentConnect is illustrated below:

<p align="center">
  <img src="/images/agent-connect-architecture.png" width="50%" alt="Project Architecture"/>
</p>

Corresponding to the three-layer architecture of the Agent Network Protocol, AgentConnect primarily includes:

1. 🔒 **Authentication and End-to-End Encryption Modules**
   Implements W3C DID-based authentication and end-to-end encrypted communication, including DID document generation, verification, retrieval, and end-to-end encryption based on DID and ECDHE (Elliptic Curve Diffie-Hellman Ephemeral). Currently supports **HTTP-based DID authentication**.

2. 🌍 **Meta-Protocol Module**
   Built on LLM (Large Language Models) and meta-protocols, this module handles application protocol negotiation, protocol code implementation, protocol debugging, and protocol processing.

3. 📡 **Application Layer Protocol Integration Framework**
   Manages protocol specifications and code for communication with other agents, including protocol loading, unloading, configuration, and processing. This framework enables agents to easily load and run required protocols on demand, accelerating protocol negotiation.

Beyond these features, AgentConnect will focus on performance and multi-platform support:

- **Performance**: As a fundamental codebase, we aim to provide optimal performance and plan to rewrite core components in Rust.
- **Multi-Platform**: Currently supports Mac, Linux, and Windows, with future support for mobile platforms and browsers.

### Documentation

- Learn more about AgentNetworkProtocol: [Agent Network Protocol (ANP)](https://github.com/chgaowei/AgentNetworkProtocol)
- For our overall design philosophy, check our technical whitepaper: [AgentNetworkProtocol Technical White Paper](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/01-AgentNetworkProtocol%20Technical%20White%20Paper.md)

Here are some of our blogs:

- This is our understanding of the agent network: [What's Different About the Agentic Web](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/blogs/What-Makes-Agentic-Web-Different.md)

- A brief introduction to did:wba: [did:wba - Web-Based Decentralized Identifiers](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/blogs/did:wba,%20a%20Web-based%20Decentralized%20Identifier.md)

- We compared the differences between did:wba and technologies like OpenID Connect and API keys: [Comparison of did:wba with OpenID Connect and API keys](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/blogs/Comparison%20of%20did:wba%20with%20OpenID%20Connect%20and%20API%20keys.md)

- We analyzed the security principles of did:wba: [Security Principles of did:wba](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/blogs/did%3Awba-security-principles.md)

- Three Technical Approaches to AI-Internet Interaction: [Three Technical Approaches to AI-Internet Interaction](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/blogs/Three_Technical_Approaches_to_AI_Internet_Interaction.md)


### Milestones

Both protocol and implementation development follow this progression:

- [x] Build authentication and end-to-end encrypted communication protocol and implementation. This foundational core is essentially complete.
- [x] Meta-protocol design and implementation. Protocol design and code development are basically complete.
- [ ] Application layer protocol design and development. Currently in progress.

To establish ANP as an industry standard, we plan to form an ANP Standardization Committee at an appropriate time, working towards recognition by international standardization organizations like W3C.

### Installation

```bash
pip install agent-connect
```

### Running

After installing the agent-connect library, you can run our demos to experience its capabilities.

Clone the repository:

```bash
git clone https://github.com/chgaowei/AgentConnect.git
```

#### Decentralized Authentication Based on did:wba and HTTP

did:wba is a Web-based Decentralized Identifier. More information: [did:wba, a Web-based Decentralized Identifier](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/blogs/did%3Awba%2C%20a%20Web-based%20Decentralized%20Identifier.md).

Our latest version supports decentralized authentication based on did:wba and HTTP. We provide a did:wba server for testing. Server API documentation: [did:wba Server Test API Documentation](https://github.com/chgaowei/AgentNetworkProtocol/blob/main/docs/did%3Awba%20server%20test%20interface.md). 

Example code path: `examples/did_wba_examples`. Including:

- basic.py: A basic example of DID WBA authentication. Creates a DID document and private key, uploads the DID document to the server, and tests DID authentication.
- full.py: Builds on basic.py, adding token verification and DID document validation.
- client.py: A client example for testing if your server supports DID WBA authentication, using pre-created DID documents and private keys.

Run these files directly to experience DID WBA authentication:

```bash
python basic.py
python full.py
python client.py
```

You can also experience DID WBA authentication through our demo page: [DID WBA Authentication Page](https://www.service.agent-network-protocol.com/wba/examples/). This page demonstrates the process of creating a DID identity on one platform (pi-unlimited.com) and then verifying the identity on another platform (service.agent-network-protocol.com).

#### Meta-Protocol Negotiation Example

We support meta-protocol negotiation where Alice and Bob first negotiate a protocol, generate processing code, and then communicate using the protocol code.

Run the demo code in examples/negotiation_mode directory. Start Bob's node first, then Alice's node.

1. Start Bob's node
```bash
python negotiation_bob.py
```

2. Start Alice's node
```bash
python negotiation_alice.py
```

The logs will show successful connection, protocol negotiation, code generation, and data communication between Alice and Bob.

> Note:
> Meta-protocol negotiation requires Azure OpenAI API configuration (currently only supports Azure OpenAI). Configure these environment variables in the ".env" file in the project root: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_MODEL_NAME

### Contact Us

Author: Gaowei Chang  
Email: chgaowei@gmail.com  
- Discord: [https://discord.gg/sFjBKTY7sB](https://discord.gg/sFjBKTY7sB)  
- Website: [https://agent-network-protocol.com/](https://agent-network-protocol.com/)  
- GitHub: [https://github.com/chgaowei/AgentNetworkProtocol](https://github.com/chgaowei/AgentNetworkProtocol)
- WeChat: flow10240

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for details.

## Copyright Notice
Copyright (c) 2024 GaoWei Chang  
This file is released under the [MIT License](./LICENSE). You are free to use and modify it, but you must retain this copyright notice.
