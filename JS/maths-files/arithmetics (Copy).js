!(function (e, t) {
	"object" == typeof exports && "object" == typeof module
		? (module.exports = t())
		: "function" == typeof define && define.amd
		? define([], t)
		: "object" == typeof exports
		? (exports.eblib = t())
		: ((e.Easybroadcast = e.Easybroadcast || {}),
		  (e.Easybroadcast.eblib = t()));
})(window, function () {
	return (function (e) {
		var t = {};
		function n(r) {
			if (t[r]) return t[r].exports;
			var i = (t[r] = { i: r, l: !1, exports: {} });
			return e[r].call(i.exports, i, i.exports, n), (i.l = !0), i.exports;
		}
		return (
			(n.m = e),
			(n.c = t),
			(n.d = function (e, t, r) {
				n.o(e, t) || Object.defineProperty(e, t, { enumerable: !0, get: r });
			}),
			(n.r = function (e) {
				"undefined" != typeof Symbol &&
					Symbol.toStringTag &&
					Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
					Object.defineProperty(e, "__esModule", { value: !0 });
			}),
			(n.t = function (e, t) {
				if ((1 & t && (e = n(e)), 8 & t)) return e;
				if (4 & t && "object" == typeof e && e && e.__esModule) return e;
				var r = Object.create(null);
				if (
					(n.r(r),
					Object.defineProperty(r, "default", { enumerable: !0, value: e }),
					2 & t && "string" != typeof e)
				)
					for (var i in e)
						n.d(
							r,
							i,
							function (t) {
								return e[t];
							}.bind(null, i)
						);
				return r;
			}),
			(n.n = function (e) {
				var t =
					e && e.__esModule
						? function () {
								return e.default;
						  }
						: function () {
								return e;
						  };
				return n.d(t, "a", t), t;
			}),
			(n.o = function (e, t) {
				return Object.prototype.hasOwnProperty.call(e, t);
			}),
			(n.p = ""),
			n((n.s = 55))
		);
	})([
		function (e, t, n) {
			"use strict";
			var r,
				i,
				o,
				s = n(17),
				a = s.Reader,
				u = s.Writer,
				c = s.util,
				l = s.roots.default || (s.roots.default = {});
			(l.manager =
				(((o = {}).IceCandidateType =
					((r = {}),
					((i = Object.create(r))[(r[0] = "CandidateTypeHost")] = 0),
					(i[(r[1] = "CandidateTypeServerReflexive")] = 1),
					(i[(r[2] = "CandidateTypePeerReflexive")] = 2),
					(i[(r[3] = "CandidateTypeRelay")] = 3),
					i)),
				(o.IceCandidate = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Type = 0),
						(e.prototype.Address = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									t.uint32(8).int32(e.Type),
								null != e.Address &&
									e.hasOwnProperty("Address") &&
									t.uint32(18).string(e.Address),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.IceCandidate();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Type = e.int32();
										break;
									case 2:
										r.Address = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.Type && e.hasOwnProperty("Type"))
								switch (e.Type) {
									default:
										return "Type: enum value expected";
									case 0:
									case 1:
									case 2:
									case 3:
								}
							return null != e.Address &&
								e.hasOwnProperty("Address") &&
								!c.isString(e.Address)
								? "Address: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.IceCandidate) return e;
							var t = new l.manager.IceCandidate();
							switch (e.Type) {
								case "CandidateTypeHost":
								case 0:
									t.Type = 0;
									break;
								case "CandidateTypeServerReflexive":
								case 1:
									t.Type = 1;
									break;
								case "CandidateTypePeerReflexive":
								case 2:
									t.Type = 2;
									break;
								case "CandidateTypeRelay":
								case 3:
									t.Type = 3;
							}
							return null != e.Address && (t.Address = String(e.Address)), t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.Type = t.enums === String ? "CandidateTypeHost" : 0),
									(n.Address = "")),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									(n.Type =
										t.enums === String
											? l.manager.IceCandidateType[e.Type]
											: e.Type),
								null != e.Address &&
									e.hasOwnProperty("Address") &&
									(n.Address = e.Address),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.MessageType = (function () {
					var e = {},
						t = Object.create(e);
					return (
						(t[(e[0] = "MessageTypeUnknown")] = 0),
						(t[(e[256] = "MessageTypeRegister")] = 256),
						(t[(e[257] = "MessageTypeUnregister")] = 257),
						(t[(e[260] = "MessageTypeImGood")] = 260),
						(t[(e[512] = "MessageTypeGiveMePeers")] = 512),
						(t[(e[513] = "MessageTypeHereAreSomePeers")] = 513),
						(t[(e[514] = "MessageTypeSwipeRight")] = 514),
						(t[(e[516] = "MessageTypeSwipeLeft")] = 516),
						(t[(e[515] = "MessageTypeItsAMatch")] = 515),
						(t[(e[518] = "MessageTypePairingRequest")] = 518),
						(t[(e[771] = "MessageTypeRegistered")] = 771),
						(t[(e[772] = "MessageTypePairingInProgress")] = 772),
						(t[(e[1025] = "MessageTypeEvent")] = 1025),
						(t[(e[1281] = "MessageTypeConf")] = 1281),
						(t[(e[1537] = "MessageTypeBytes")] = 1537),
						t
					);
				})()),
				(o.ArgumentsHereAreSomePeers = (function () {
					function e(e) {
						if (((this.Peers = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Peers = c.emptyArray),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if ((t || (t = u.create()), null != e.Peers && e.Peers.length))
								for (var n = 0; n < e.Peers.length; ++n)
									t.uint32(10).string(e.Peers[n]);
							return t;
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsHereAreSomePeers();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										(r.Peers && r.Peers.length) || (r.Peers = []),
											r.Peers.push(e.string());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.Peers && e.hasOwnProperty("Peers")) {
								if (!Array.isArray(e.Peers)) return "Peers: array expected";
								for (var t = 0; t < e.Peers.length; ++t)
									if (!c.isString(e.Peers[t]))
										return "Peers: string[] expected";
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsHereAreSomePeers) return e;
							var t = new l.manager.ArgumentsHereAreSomePeers();
							if (e.Peers) {
								if (!Array.isArray(e.Peers))
									throw TypeError(
										".manager.ArgumentsHereAreSomePeers.Peers: array expected"
									);
								t.Peers = [];
								for (var n = 0; n < e.Peers.length; ++n)
									t.Peers[n] = String(e.Peers[n]);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Peers = []),
								e.Peers && e.Peers.length)
							) {
								n.Peers = [];
								for (var r = 0; r < e.Peers.length; ++r)
									n.Peers[r] = e.Peers[r];
							}
							return n;
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsItsAMatch = (function () {
					function e(e) {
						if (((this.Candidates = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Peer = ""),
						(e.prototype.Offer = ""),
						(e.prototype.Candidates = c.emptyArray),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if (
								(t || (t = u.create()),
								null != e.Peer &&
									e.hasOwnProperty("Peer") &&
									t.uint32(10).string(e.Peer),
								null != e.Offer &&
									e.hasOwnProperty("Offer") &&
									t.uint32(18).string(e.Offer),
								null != e.Candidates && e.Candidates.length)
							)
								for (var n = 0; n < e.Candidates.length; ++n)
									t.uint32(26).string(e.Candidates[n]);
							return t;
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsItsAMatch();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Peer = e.string();
										break;
									case 2:
										r.Offer = e.string();
										break;
									case 3:
										(r.Candidates && r.Candidates.length) ||
											(r.Candidates = []),
											r.Candidates.push(e.string());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.Peer &&
								e.hasOwnProperty("Peer") &&
								!c.isString(e.Peer)
							)
								return "Peer: string expected";
							if (
								null != e.Offer &&
								e.hasOwnProperty("Offer") &&
								!c.isString(e.Offer)
							)
								return "Offer: string expected";
							if (null != e.Candidates && e.hasOwnProperty("Candidates")) {
								if (!Array.isArray(e.Candidates))
									return "Candidates: array expected";
								for (var t = 0; t < e.Candidates.length; ++t)
									if (!c.isString(e.Candidates[t]))
										return "Candidates: string[] expected";
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsItsAMatch) return e;
							var t = new l.manager.ArgumentsItsAMatch();
							if (
								(null != e.Peer && (t.Peer = String(e.Peer)),
								null != e.Offer && (t.Offer = String(e.Offer)),
								e.Candidates)
							) {
								if (!Array.isArray(e.Candidates))
									throw TypeError(
										".manager.ArgumentsItsAMatch.Candidates: array expected"
									);
								t.Candidates = [];
								for (var n = 0; n < e.Candidates.length; ++n)
									t.Candidates[n] = String(e.Candidates[n]);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Candidates = []),
								t.defaults && ((n.Peer = ""), (n.Offer = "")),
								null != e.Peer && e.hasOwnProperty("Peer") && (n.Peer = e.Peer),
								null != e.Offer &&
									e.hasOwnProperty("Offer") &&
									(n.Offer = e.Offer),
								e.Candidates && e.Candidates.length)
							) {
								n.Candidates = [];
								for (var r = 0; r < e.Candidates.length; ++r)
									n.Candidates[r] = e.Candidates[r];
							}
							return n;
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PairingRequestType = (function () {
					var e = {},
						t = Object.create(e);
					return (
						(t[(e[0] = "PairingRequestType_offer")] = 0),
						(t[(e[1] = "PairingRequestType_answer")] = 1),
						t
					);
				})()),
				(o.ArgumentsPairingRequest = (function () {
					function e(e) {
						if (((this.Candidates = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Type = 0),
						(e.prototype.Peer = ""),
						(e.prototype.Offer = ""),
						(e.prototype.Candidates = c.emptyArray),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if (
								(t || (t = u.create()),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									t.uint32(8).int32(e.Type),
								null != e.Peer &&
									e.hasOwnProperty("Peer") &&
									t.uint32(18).string(e.Peer),
								null != e.Offer &&
									e.hasOwnProperty("Offer") &&
									t.uint32(26).string(e.Offer),
								null != e.Candidates && e.Candidates.length)
							)
								for (var n = 0; n < e.Candidates.length; ++n)
									t.uint32(34).string(e.Candidates[n]);
							return t;
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsPairingRequest();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Type = e.int32();
										break;
									case 2:
										r.Peer = e.string();
										break;
									case 3:
										r.Offer = e.string();
										break;
									case 4:
										(r.Candidates && r.Candidates.length) ||
											(r.Candidates = []),
											r.Candidates.push(e.string());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.Type && e.hasOwnProperty("Type"))
								switch (e.Type) {
									default:
										return "Type: enum value expected";
									case 0:
									case 1:
								}
							if (
								null != e.Peer &&
								e.hasOwnProperty("Peer") &&
								!c.isString(e.Peer)
							)
								return "Peer: string expected";
							if (
								null != e.Offer &&
								e.hasOwnProperty("Offer") &&
								!c.isString(e.Offer)
							)
								return "Offer: string expected";
							if (null != e.Candidates && e.hasOwnProperty("Candidates")) {
								if (!Array.isArray(e.Candidates))
									return "Candidates: array expected";
								for (var t = 0; t < e.Candidates.length; ++t)
									if (!c.isString(e.Candidates[t]))
										return "Candidates: string[] expected";
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsPairingRequest) return e;
							var t = new l.manager.ArgumentsPairingRequest();
							switch (e.Type) {
								case "PairingRequestType_offer":
								case 0:
									t.Type = 0;
									break;
								case "PairingRequestType_answer":
								case 1:
									t.Type = 1;
							}
							if (
								(null != e.Peer && (t.Peer = String(e.Peer)),
								null != e.Offer && (t.Offer = String(e.Offer)),
								e.Candidates)
							) {
								if (!Array.isArray(e.Candidates))
									throw TypeError(
										".manager.ArgumentsPairingRequest.Candidates: array expected"
									);
								t.Candidates = [];
								for (var n = 0; n < e.Candidates.length; ++n)
									t.Candidates[n] = String(e.Candidates[n]);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Candidates = []),
								t.defaults &&
									((n.Type =
										t.enums === String ? "PairingRequestType_offer" : 0),
									(n.Peer = ""),
									(n.Offer = "")),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									(n.Type =
										t.enums === String
											? l.manager.PairingRequestType[e.Type]
											: e.Type),
								null != e.Peer && e.hasOwnProperty("Peer") && (n.Peer = e.Peer),
								null != e.Offer &&
									e.hasOwnProperty("Offer") &&
									(n.Offer = e.Offer),
								e.Candidates && e.Candidates.length)
							) {
								n.Candidates = [];
								for (var r = 0; r < e.Candidates.length; ++r)
									n.Candidates[r] = e.Candidates[r];
							}
							return n;
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsSwipeRight = (function () {
					function e(e) {
						if (((this.Candidates = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Peer = ""),
						(e.prototype.Offer = ""),
						(e.prototype.Candidates = c.emptyArray),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if (
								(t || (t = u.create()),
								null != e.Peer &&
									e.hasOwnProperty("Peer") &&
									t.uint32(10).string(e.Peer),
								null != e.Offer &&
									e.hasOwnProperty("Offer") &&
									t.uint32(18).string(e.Offer),
								null != e.Candidates && e.Candidates.length)
							)
								for (var n = 0; n < e.Candidates.length; ++n)
									t.uint32(26).string(e.Candidates[n]);
							return t;
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsSwipeRight();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Peer = e.string();
										break;
									case 2:
										r.Offer = e.string();
										break;
									case 3:
										(r.Candidates && r.Candidates.length) ||
											(r.Candidates = []),
											r.Candidates.push(e.string());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.Peer &&
								e.hasOwnProperty("Peer") &&
								!c.isString(e.Peer)
							)
								return "Peer: string expected";
							if (
								null != e.Offer &&
								e.hasOwnProperty("Offer") &&
								!c.isString(e.Offer)
							)
								return "Offer: string expected";
							if (null != e.Candidates && e.hasOwnProperty("Candidates")) {
								if (!Array.isArray(e.Candidates))
									return "Candidates: array expected";
								for (var t = 0; t < e.Candidates.length; ++t)
									if (!c.isString(e.Candidates[t]))
										return "Candidates: string[] expected";
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsSwipeRight) return e;
							var t = new l.manager.ArgumentsSwipeRight();
							if (
								(null != e.Peer && (t.Peer = String(e.Peer)),
								null != e.Offer && (t.Offer = String(e.Offer)),
								e.Candidates)
							) {
								if (!Array.isArray(e.Candidates))
									throw TypeError(
										".manager.ArgumentsSwipeRight.Candidates: array expected"
									);
								t.Candidates = [];
								for (var n = 0; n < e.Candidates.length; ++n)
									t.Candidates[n] = String(e.Candidates[n]);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Candidates = []),
								t.defaults && ((n.Peer = ""), (n.Offer = "")),
								null != e.Peer && e.hasOwnProperty("Peer") && (n.Peer = e.Peer),
								null != e.Offer &&
									e.hasOwnProperty("Offer") &&
									(n.Offer = e.Offer),
								e.Candidates && e.Candidates.length)
							) {
								n.Candidates = [];
								for (var r = 0; r < e.Candidates.length; ++r)
									n.Candidates[r] = e.Candidates[r];
							}
							return n;
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsGiveMePeers = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Current = 0),
						(e.prototype.CDNThroughput = 0),
						(e.prototype.Want = 0),
						(e.prototype.Accept = 0),
						(e.prototype.CurrentTime = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Current &&
									e.hasOwnProperty("Current") &&
									t.uint32(8).uint32(e.Current),
								null != e.CDNThroughput &&
									e.hasOwnProperty("CDNThroughput") &&
									t.uint32(21).float(e.CDNThroughput),
								null != e.Want &&
									e.hasOwnProperty("Want") &&
									t.uint32(24).uint32(e.Want),
								null != e.Accept &&
									e.hasOwnProperty("Accept") &&
									t.uint32(32).uint32(e.Accept),
								null != e.CurrentTime &&
									e.hasOwnProperty("CurrentTime") &&
									t.uint32(45).float(e.CurrentTime),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsGiveMePeers();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Current = e.uint32();
										break;
									case 2:
										r.CDNThroughput = e.float();
										break;
									case 3:
										r.Want = e.uint32();
										break;
									case 4:
										r.Accept = e.uint32();
										break;
									case 5:
										r.CurrentTime = e.float();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Current &&
								  e.hasOwnProperty("Current") &&
								  !c.isInteger(e.Current)
								? "Current: integer expected"
								: null != e.CDNThroughput &&
								  e.hasOwnProperty("CDNThroughput") &&
								  "number" != typeof e.CDNThroughput
								? "CDNThroughput: number expected"
								: null != e.Want &&
								  e.hasOwnProperty("Want") &&
								  !c.isInteger(e.Want)
								? "Want: integer expected"
								: null != e.Accept &&
								  e.hasOwnProperty("Accept") &&
								  !c.isInteger(e.Accept)
								? "Accept: integer expected"
								: null != e.CurrentTime &&
								  e.hasOwnProperty("CurrentTime") &&
								  "number" != typeof e.CurrentTime
								? "CurrentTime: number expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsGiveMePeers) return e;
							var t = new l.manager.ArgumentsGiveMePeers();
							return (
								null != e.Current && (t.Current = e.Current >>> 0),
								null != e.CDNThroughput &&
									(t.CDNThroughput = Number(e.CDNThroughput)),
								null != e.Want && (t.Want = e.Want >>> 0),
								null != e.Accept && (t.Accept = e.Accept >>> 0),
								null != e.CurrentTime &&
									(t.CurrentTime = Number(e.CurrentTime)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.Current = 0),
									(n.CDNThroughput = 0),
									(n.Want = 0),
									(n.Accept = 0),
									(n.CurrentTime = 0)),
								null != e.Current &&
									e.hasOwnProperty("Current") &&
									(n.Current = e.Current),
								null != e.CDNThroughput &&
									e.hasOwnProperty("CDNThroughput") &&
									(n.CDNThroughput =
										t.json && !isFinite(e.CDNThroughput)
											? String(e.CDNThroughput)
											: e.CDNThroughput),
								null != e.Want && e.hasOwnProperty("Want") && (n.Want = e.Want),
								null != e.Accept &&
									e.hasOwnProperty("Accept") &&
									(n.Accept = e.Accept),
								null != e.CurrentTime &&
									e.hasOwnProperty("CurrentTime") &&
									(n.CurrentTime =
										t.json && !isFinite(e.CurrentTime)
											? String(e.CurrentTime)
											: e.CurrentTime),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.SwipeLeftReason = (function () {
					var e = {},
						t = Object.create(e);
					return (
						(t[(e[0] = "UnknownSwipeLeftReason")] = 0),
						(t[(e[1] = "SwipeLeftNotReachable")] = 1),
						(t[(e[2] = "SwipeLeftTimedOut")] = 2),
						(t[(e[3] = "SwipeLeftNotInteresting")] = 3),
						t
					);
				})()),
				(o.ArgumentsSwipeLeft = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Peer = ""),
						(e.prototype.Reason = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Peer &&
									e.hasOwnProperty("Peer") &&
									t.uint32(10).string(e.Peer),
								null != e.Reason &&
									e.hasOwnProperty("Reason") &&
									t.uint32(16).int32(e.Reason),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsSwipeLeft();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Peer = e.string();
										break;
									case 2:
										r.Reason = e.int32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.Peer &&
								e.hasOwnProperty("Peer") &&
								!c.isString(e.Peer)
							)
								return "Peer: string expected";
							if (null != e.Reason && e.hasOwnProperty("Reason"))
								switch (e.Reason) {
									default:
										return "Reason: enum value expected";
									case 0:
									case 1:
									case 2:
									case 3:
								}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsSwipeLeft) return e;
							var t = new l.manager.ArgumentsSwipeLeft();
							switch ((null != e.Peer && (t.Peer = String(e.Peer)), e.Reason)) {
								case "UnknownSwipeLeftReason":
								case 0:
									t.Reason = 0;
									break;
								case "SwipeLeftNotReachable":
								case 1:
									t.Reason = 1;
									break;
								case "SwipeLeftTimedOut":
								case 2:
									t.Reason = 2;
									break;
								case "SwipeLeftNotInteresting":
								case 3:
									t.Reason = 3;
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.Peer = ""),
									(n.Reason =
										t.enums === String ? "UnknownSwipeLeftReason" : 0)),
								null != e.Peer && e.hasOwnProperty("Peer") && (n.Peer = e.Peer),
								null != e.Reason &&
									e.hasOwnProperty("Reason") &&
									(n.Reason =
										t.enums === String
											? l.manager.SwipeLeftReason[e.Reason]
											: e.Reason),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsBytes = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.MetricVersion = ""),
						(e.prototype.Bytes = c.newBuffer([])),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.MetricVersion &&
									e.hasOwnProperty("MetricVersion") &&
									t.uint32(10).string(e.MetricVersion),
								null != e.Bytes &&
									e.hasOwnProperty("Bytes") &&
									t.uint32(18).bytes(e.Bytes),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsBytes();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.MetricVersion = e.string();
										break;
									case 2:
										r.Bytes = e.bytes();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.MetricVersion &&
								  e.hasOwnProperty("MetricVersion") &&
								  !c.isString(e.MetricVersion)
								? "MetricVersion: string expected"
								: null != e.Bytes &&
								  e.hasOwnProperty("Bytes") &&
								  !(
										(e.Bytes && "number" == typeof e.Bytes.length) ||
										c.isString(e.Bytes)
								  )
								? "Bytes: buffer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsBytes) return e;
							var t = new l.manager.ArgumentsBytes();
							return (
								null != e.MetricVersion &&
									(t.MetricVersion = String(e.MetricVersion)),
								null != e.Bytes &&
									("string" == typeof e.Bytes
										? c.base64.decode(
												e.Bytes,
												(t.Bytes = c.newBuffer(c.base64.length(e.Bytes))),
												0
										  )
										: e.Bytes.length && (t.Bytes = e.Bytes)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.MetricVersion = ""),
									t.bytes === String
										? (n.Bytes = "")
										: ((n.Bytes = []),
										  t.bytes !== Array && (n.Bytes = c.newBuffer(n.Bytes)))),
								null != e.MetricVersion &&
									e.hasOwnProperty("MetricVersion") &&
									(n.MetricVersion = e.MetricVersion),
								null != e.Bytes &&
									e.hasOwnProperty("Bytes") &&
									(n.Bytes =
										t.bytes === String
											? c.base64.encode(e.Bytes, 0, e.Bytes.length)
											: t.bytes === Array
											? Array.prototype.slice.call(e.Bytes)
											: e.Bytes),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.Message = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					var t;
					return (
						(e.prototype.Type = 0),
						(e.prototype.Timestamp = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.PeerID = ""),
						(e.prototype.ArgumentsRegister = null),
						(e.prototype.ArgumentsUnregister = null),
						(e.prototype.ArgumentsHereAreSomePeers = null),
						(e.prototype.ArgumentsSwipeRight = null),
						(e.prototype.ArgumentsItsAMatch = null),
						(e.prototype.ArgumentsSwipeLeft = null),
						(e.prototype.ArgumentsPairingRequest = null),
						(e.prototype.ArgumentsRegistered = null),
						(e.prototype.ArgumentsEvent = null),
						(e.prototype.ArgumentsConf = null),
						(e.prototype.ArgumentsBytes = null),
						(e.prototype.ArgumentsGiveMePeers = null),
						Object.defineProperty(e.prototype, "Arguments", {
							get: c.oneOfGetter(
								(t = [
									"ArgumentsRegister",
									"ArgumentsUnregister",
									"ArgumentsHereAreSomePeers",
									"ArgumentsSwipeRight",
									"ArgumentsItsAMatch",
									"ArgumentsSwipeLeft",
									"ArgumentsPairingRequest",
									"ArgumentsRegistered",
									"ArgumentsEvent",
									"ArgumentsConf",
									"ArgumentsBytes",
									"ArgumentsGiveMePeers",
								])
							),
							set: c.oneOfSetter(t),
						}),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									t.uint32(8).int32(e.Type),
								null != e.Timestamp &&
									e.hasOwnProperty("Timestamp") &&
									t.uint32(16).int64(e.Timestamp),
								null != e.PeerID &&
									e.hasOwnProperty("PeerID") &&
									t.uint32(26).string(e.PeerID),
								null != e.ArgumentsRegister &&
									e.hasOwnProperty("ArgumentsRegister") &&
									l.manager.ArgumentsRegister.encode(
										e.ArgumentsRegister,
										t.uint32(82).fork()
									).ldelim(),
								null != e.ArgumentsUnregister &&
									e.hasOwnProperty("ArgumentsUnregister") &&
									l.manager.ArgumentsUnregister.encode(
										e.ArgumentsUnregister,
										t.uint32(90).fork()
									).ldelim(),
								null != e.ArgumentsHereAreSomePeers &&
									e.hasOwnProperty("ArgumentsHereAreSomePeers") &&
									l.manager.ArgumentsHereAreSomePeers.encode(
										e.ArgumentsHereAreSomePeers,
										t.uint32(114).fork()
									).ldelim(),
								null != e.ArgumentsSwipeRight &&
									e.hasOwnProperty("ArgumentsSwipeRight") &&
									l.manager.ArgumentsSwipeRight.encode(
										e.ArgumentsSwipeRight,
										t.uint32(122).fork()
									).ldelim(),
								null != e.ArgumentsItsAMatch &&
									e.hasOwnProperty("ArgumentsItsAMatch") &&
									l.manager.ArgumentsItsAMatch.encode(
										e.ArgumentsItsAMatch,
										t.uint32(130).fork()
									).ldelim(),
								null != e.ArgumentsSwipeLeft &&
									e.hasOwnProperty("ArgumentsSwipeLeft") &&
									l.manager.ArgumentsSwipeLeft.encode(
										e.ArgumentsSwipeLeft,
										t.uint32(138).fork()
									).ldelim(),
								null != e.ArgumentsPairingRequest &&
									e.hasOwnProperty("ArgumentsPairingRequest") &&
									l.manager.ArgumentsPairingRequest.encode(
										e.ArgumentsPairingRequest,
										t.uint32(170).fork()
									).ldelim(),
								null != e.ArgumentsRegistered &&
									e.hasOwnProperty("ArgumentsRegistered") &&
									l.manager.ArgumentsRegistered.encode(
										e.ArgumentsRegistered,
										t.uint32(178).fork()
									).ldelim(),
								null != e.ArgumentsEvent &&
									e.hasOwnProperty("ArgumentsEvent") &&
									l.manager.ArgumentsEvent.encode(
										e.ArgumentsEvent,
										t.uint32(202).fork()
									).ldelim(),
								null != e.ArgumentsConf &&
									e.hasOwnProperty("ArgumentsConf") &&
									l.manager.ArgumentsConf.encode(
										e.ArgumentsConf,
										t.uint32(210).fork()
									).ldelim(),
								null != e.ArgumentsBytes &&
									e.hasOwnProperty("ArgumentsBytes") &&
									l.manager.ArgumentsBytes.encode(
										e.ArgumentsBytes,
										t.uint32(218).fork()
									).ldelim(),
								null != e.ArgumentsGiveMePeers &&
									e.hasOwnProperty("ArgumentsGiveMePeers") &&
									l.manager.ArgumentsGiveMePeers.encode(
										e.ArgumentsGiveMePeers,
										t.uint32(226).fork()
									).ldelim(),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.Message();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Type = e.int32();
										break;
									case 2:
										r.Timestamp = e.int64();
										break;
									case 3:
										r.PeerID = e.string();
										break;
									case 10:
										r.ArgumentsRegister = l.manager.ArgumentsRegister.decode(
											e,
											e.uint32()
										);
										break;
									case 11:
										r.ArgumentsUnregister =
											l.manager.ArgumentsUnregister.decode(e, e.uint32());
										break;
									case 14:
										r.ArgumentsHereAreSomePeers =
											l.manager.ArgumentsHereAreSomePeers.decode(e, e.uint32());
										break;
									case 15:
										r.ArgumentsSwipeRight =
											l.manager.ArgumentsSwipeRight.decode(e, e.uint32());
										break;
									case 16:
										r.ArgumentsItsAMatch = l.manager.ArgumentsItsAMatch.decode(
											e,
											e.uint32()
										);
										break;
									case 17:
										r.ArgumentsSwipeLeft = l.manager.ArgumentsSwipeLeft.decode(
											e,
											e.uint32()
										);
										break;
									case 21:
										r.ArgumentsPairingRequest =
											l.manager.ArgumentsPairingRequest.decode(e, e.uint32());
										break;
									case 22:
										r.ArgumentsRegistered =
											l.manager.ArgumentsRegistered.decode(e, e.uint32());
										break;
									case 25:
										r.ArgumentsEvent = l.manager.ArgumentsEvent.decode(
											e,
											e.uint32()
										);
										break;
									case 26:
										r.ArgumentsConf = l.manager.ArgumentsConf.decode(
											e,
											e.uint32()
										);
										break;
									case 27:
										r.ArgumentsBytes = l.manager.ArgumentsBytes.decode(
											e,
											e.uint32()
										);
										break;
									case 28:
										r.ArgumentsGiveMePeers =
											l.manager.ArgumentsGiveMePeers.decode(e, e.uint32());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							var t = {};
							if (null != e.Type && e.hasOwnProperty("Type"))
								switch (e.Type) {
									default:
										return "Type: enum value expected";
									case 0:
									case 256:
									case 257:
									case 260:
									case 512:
									case 513:
									case 514:
									case 516:
									case 515:
									case 518:
									case 771:
									case 772:
									case 1025:
									case 1281:
									case 1537:
								}
							if (
								null != e.Timestamp &&
								e.hasOwnProperty("Timestamp") &&
								!(
									c.isInteger(e.Timestamp) ||
									(e.Timestamp &&
										c.isInteger(e.Timestamp.low) &&
										c.isInteger(e.Timestamp.high))
								)
							)
								return "Timestamp: integer|Long expected";
							if (
								null != e.PeerID &&
								e.hasOwnProperty("PeerID") &&
								!c.isString(e.PeerID)
							)
								return "PeerID: string expected";
							if (
								null != e.ArgumentsRegister &&
								e.hasOwnProperty("ArgumentsRegister") &&
								((t.Arguments = 1),
								(n = l.manager.ArgumentsRegister.verify(e.ArgumentsRegister)))
							)
								return "ArgumentsRegister." + n;
							if (
								null != e.ArgumentsUnregister &&
								e.hasOwnProperty("ArgumentsUnregister")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsUnregister.verify(
										e.ArgumentsUnregister
									)))
								)
									return "ArgumentsUnregister." + n;
							}
							if (
								null != e.ArgumentsHereAreSomePeers &&
								e.hasOwnProperty("ArgumentsHereAreSomePeers")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsHereAreSomePeers.verify(
										e.ArgumentsHereAreSomePeers
									)))
								)
									return "ArgumentsHereAreSomePeers." + n;
							}
							if (
								null != e.ArgumentsSwipeRight &&
								e.hasOwnProperty("ArgumentsSwipeRight")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsSwipeRight.verify(
										e.ArgumentsSwipeRight
									)))
								)
									return "ArgumentsSwipeRight." + n;
							}
							if (
								null != e.ArgumentsItsAMatch &&
								e.hasOwnProperty("ArgumentsItsAMatch")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsItsAMatch.verify(
										e.ArgumentsItsAMatch
									)))
								)
									return "ArgumentsItsAMatch." + n;
							}
							if (
								null != e.ArgumentsSwipeLeft &&
								e.hasOwnProperty("ArgumentsSwipeLeft")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsSwipeLeft.verify(
										e.ArgumentsSwipeLeft
									)))
								)
									return "ArgumentsSwipeLeft." + n;
							}
							if (
								null != e.ArgumentsPairingRequest &&
								e.hasOwnProperty("ArgumentsPairingRequest")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsPairingRequest.verify(
										e.ArgumentsPairingRequest
									)))
								)
									return "ArgumentsPairingRequest." + n;
							}
							if (
								null != e.ArgumentsRegistered &&
								e.hasOwnProperty("ArgumentsRegistered")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsRegistered.verify(
										e.ArgumentsRegistered
									)))
								)
									return "ArgumentsRegistered." + n;
							}
							if (
								null != e.ArgumentsEvent &&
								e.hasOwnProperty("ArgumentsEvent")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsEvent.verify(e.ArgumentsEvent)))
								)
									return "ArgumentsEvent." + n;
							}
							if (
								null != e.ArgumentsConf &&
								e.hasOwnProperty("ArgumentsConf")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsConf.verify(e.ArgumentsConf)))
								)
									return "ArgumentsConf." + n;
							}
							if (
								null != e.ArgumentsBytes &&
								e.hasOwnProperty("ArgumentsBytes")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsBytes.verify(e.ArgumentsBytes)))
								)
									return "ArgumentsBytes." + n;
							}
							if (
								null != e.ArgumentsGiveMePeers &&
								e.hasOwnProperty("ArgumentsGiveMePeers")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								var n;
								if (
									((t.Arguments = 1),
									(n = l.manager.ArgumentsGiveMePeers.verify(
										e.ArgumentsGiveMePeers
									)))
								)
									return "ArgumentsGiveMePeers." + n;
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.Message) return e;
							var t = new l.manager.Message();
							switch (e.Type) {
								case "MessageTypeUnknown":
								case 0:
									t.Type = 0;
									break;
								case "MessageTypeRegister":
								case 256:
									t.Type = 256;
									break;
								case "MessageTypeUnregister":
								case 257:
									t.Type = 257;
									break;
								case "MessageTypeImGood":
								case 260:
									t.Type = 260;
									break;
								case "MessageTypeGiveMePeers":
								case 512:
									t.Type = 512;
									break;
								case "MessageTypeHereAreSomePeers":
								case 513:
									t.Type = 513;
									break;
								case "MessageTypeSwipeRight":
								case 514:
									t.Type = 514;
									break;
								case "MessageTypeSwipeLeft":
								case 516:
									t.Type = 516;
									break;
								case "MessageTypeItsAMatch":
								case 515:
									t.Type = 515;
									break;
								case "MessageTypePairingRequest":
								case 518:
									t.Type = 518;
									break;
								case "MessageTypeRegistered":
								case 771:
									t.Type = 771;
									break;
								case "MessageTypePairingInProgress":
								case 772:
									t.Type = 772;
									break;
								case "MessageTypeEvent":
								case 1025:
									t.Type = 1025;
									break;
								case "MessageTypeConf":
								case 1281:
									t.Type = 1281;
									break;
								case "MessageTypeBytes":
								case 1537:
									t.Type = 1537;
							}
							if (
								(null != e.Timestamp &&
									(c.Long
										? ((t.Timestamp = c.Long.fromValue(e.Timestamp)).unsigned =
												!1)
										: "string" == typeof e.Timestamp
										? (t.Timestamp = parseInt(e.Timestamp, 10))
										: "number" == typeof e.Timestamp
										? (t.Timestamp = e.Timestamp)
										: "object" == typeof e.Timestamp &&
										  (t.Timestamp = new c.LongBits(
												e.Timestamp.low >>> 0,
												e.Timestamp.high >>> 0
										  ).toNumber())),
								null != e.PeerID && (t.PeerID = String(e.PeerID)),
								null != e.ArgumentsRegister)
							) {
								if ("object" != typeof e.ArgumentsRegister)
									throw TypeError(
										".manager.Message.ArgumentsRegister: object expected"
									);
								t.ArgumentsRegister = l.manager.ArgumentsRegister.fromObject(
									e.ArgumentsRegister
								);
							}
							if (null != e.ArgumentsUnregister) {
								if ("object" != typeof e.ArgumentsUnregister)
									throw TypeError(
										".manager.Message.ArgumentsUnregister: object expected"
									);
								t.ArgumentsUnregister =
									l.manager.ArgumentsUnregister.fromObject(
										e.ArgumentsUnregister
									);
							}
							if (null != e.ArgumentsHereAreSomePeers) {
								if ("object" != typeof e.ArgumentsHereAreSomePeers)
									throw TypeError(
										".manager.Message.ArgumentsHereAreSomePeers: object expected"
									);
								t.ArgumentsHereAreSomePeers =
									l.manager.ArgumentsHereAreSomePeers.fromObject(
										e.ArgumentsHereAreSomePeers
									);
							}
							if (null != e.ArgumentsSwipeRight) {
								if ("object" != typeof e.ArgumentsSwipeRight)
									throw TypeError(
										".manager.Message.ArgumentsSwipeRight: object expected"
									);
								t.ArgumentsSwipeRight =
									l.manager.ArgumentsSwipeRight.fromObject(
										e.ArgumentsSwipeRight
									);
							}
							if (null != e.ArgumentsItsAMatch) {
								if ("object" != typeof e.ArgumentsItsAMatch)
									throw TypeError(
										".manager.Message.ArgumentsItsAMatch: object expected"
									);
								t.ArgumentsItsAMatch = l.manager.ArgumentsItsAMatch.fromObject(
									e.ArgumentsItsAMatch
								);
							}
							if (null != e.ArgumentsSwipeLeft) {
								if ("object" != typeof e.ArgumentsSwipeLeft)
									throw TypeError(
										".manager.Message.ArgumentsSwipeLeft: object expected"
									);
								t.ArgumentsSwipeLeft = l.manager.ArgumentsSwipeLeft.fromObject(
									e.ArgumentsSwipeLeft
								);
							}
							if (null != e.ArgumentsPairingRequest) {
								if ("object" != typeof e.ArgumentsPairingRequest)
									throw TypeError(
										".manager.Message.ArgumentsPairingRequest: object expected"
									);
								t.ArgumentsPairingRequest =
									l.manager.ArgumentsPairingRequest.fromObject(
										e.ArgumentsPairingRequest
									);
							}
							if (null != e.ArgumentsRegistered) {
								if ("object" != typeof e.ArgumentsRegistered)
									throw TypeError(
										".manager.Message.ArgumentsRegistered: object expected"
									);
								t.ArgumentsRegistered =
									l.manager.ArgumentsRegistered.fromObject(
										e.ArgumentsRegistered
									);
							}
							if (null != e.ArgumentsEvent) {
								if ("object" != typeof e.ArgumentsEvent)
									throw TypeError(
										".manager.Message.ArgumentsEvent: object expected"
									);
								t.ArgumentsEvent = l.manager.ArgumentsEvent.fromObject(
									e.ArgumentsEvent
								);
							}
							if (null != e.ArgumentsConf) {
								if ("object" != typeof e.ArgumentsConf)
									throw TypeError(
										".manager.Message.ArgumentsConf: object expected"
									);
								t.ArgumentsConf = l.manager.ArgumentsConf.fromObject(
									e.ArgumentsConf
								);
							}
							if (null != e.ArgumentsBytes) {
								if ("object" != typeof e.ArgumentsBytes)
									throw TypeError(
										".manager.Message.ArgumentsBytes: object expected"
									);
								t.ArgumentsBytes = l.manager.ArgumentsBytes.fromObject(
									e.ArgumentsBytes
								);
							}
							if (null != e.ArgumentsGiveMePeers) {
								if ("object" != typeof e.ArgumentsGiveMePeers)
									throw TypeError(
										".manager.Message.ArgumentsGiveMePeers: object expected"
									);
								t.ArgumentsGiveMePeers =
									l.manager.ArgumentsGiveMePeers.fromObject(
										e.ArgumentsGiveMePeers
									);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (
									((n.Type = t.enums === String ? "MessageTypeUnknown" : 0),
									c.Long)
								) {
									var r = new c.Long(0, 0, !1);
									n.Timestamp =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Timestamp = t.longs === String ? "0" : 0;
								n.PeerID = "";
							}
							return (
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									(n.Type =
										t.enums === String
											? l.manager.MessageType[e.Type]
											: e.Type),
								null != e.Timestamp &&
									e.hasOwnProperty("Timestamp") &&
									("number" == typeof e.Timestamp
										? (n.Timestamp =
												t.longs === String ? String(e.Timestamp) : e.Timestamp)
										: (n.Timestamp =
												t.longs === String
													? c.Long.prototype.toString.call(e.Timestamp)
													: t.longs === Number
													? new c.LongBits(
															e.Timestamp.low >>> 0,
															e.Timestamp.high >>> 0
													  ).toNumber()
													: e.Timestamp)),
								null != e.PeerID &&
									e.hasOwnProperty("PeerID") &&
									(n.PeerID = e.PeerID),
								null != e.ArgumentsRegister &&
									e.hasOwnProperty("ArgumentsRegister") &&
									((n.ArgumentsRegister = l.manager.ArgumentsRegister.toObject(
										e.ArgumentsRegister,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsRegister")),
								null != e.ArgumentsUnregister &&
									e.hasOwnProperty("ArgumentsUnregister") &&
									((n.ArgumentsUnregister =
										l.manager.ArgumentsUnregister.toObject(
											e.ArgumentsUnregister,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsUnregister")),
								null != e.ArgumentsHereAreSomePeers &&
									e.hasOwnProperty("ArgumentsHereAreSomePeers") &&
									((n.ArgumentsHereAreSomePeers =
										l.manager.ArgumentsHereAreSomePeers.toObject(
											e.ArgumentsHereAreSomePeers,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsHereAreSomePeers")),
								null != e.ArgumentsSwipeRight &&
									e.hasOwnProperty("ArgumentsSwipeRight") &&
									((n.ArgumentsSwipeRight =
										l.manager.ArgumentsSwipeRight.toObject(
											e.ArgumentsSwipeRight,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsSwipeRight")),
								null != e.ArgumentsItsAMatch &&
									e.hasOwnProperty("ArgumentsItsAMatch") &&
									((n.ArgumentsItsAMatch =
										l.manager.ArgumentsItsAMatch.toObject(
											e.ArgumentsItsAMatch,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsItsAMatch")),
								null != e.ArgumentsSwipeLeft &&
									e.hasOwnProperty("ArgumentsSwipeLeft") &&
									((n.ArgumentsSwipeLeft =
										l.manager.ArgumentsSwipeLeft.toObject(
											e.ArgumentsSwipeLeft,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsSwipeLeft")),
								null != e.ArgumentsPairingRequest &&
									e.hasOwnProperty("ArgumentsPairingRequest") &&
									((n.ArgumentsPairingRequest =
										l.manager.ArgumentsPairingRequest.toObject(
											e.ArgumentsPairingRequest,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsPairingRequest")),
								null != e.ArgumentsRegistered &&
									e.hasOwnProperty("ArgumentsRegistered") &&
									((n.ArgumentsRegistered =
										l.manager.ArgumentsRegistered.toObject(
											e.ArgumentsRegistered,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsRegistered")),
								null != e.ArgumentsEvent &&
									e.hasOwnProperty("ArgumentsEvent") &&
									((n.ArgumentsEvent = l.manager.ArgumentsEvent.toObject(
										e.ArgumentsEvent,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsEvent")),
								null != e.ArgumentsConf &&
									e.hasOwnProperty("ArgumentsConf") &&
									((n.ArgumentsConf = l.manager.ArgumentsConf.toObject(
										e.ArgumentsConf,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsConf")),
								null != e.ArgumentsBytes &&
									e.hasOwnProperty("ArgumentsBytes") &&
									((n.ArgumentsBytes = l.manager.ArgumentsBytes.toObject(
										e.ArgumentsBytes,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsBytes")),
								null != e.ArgumentsGiveMePeers &&
									e.hasOwnProperty("ArgumentsGiveMePeers") &&
									((n.ArgumentsGiveMePeers =
										l.manager.ArgumentsGiveMePeers.toObject(
											e.ArgumentsGiveMePeers,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsGiveMePeers")),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsConf = (function () {
					function e(e) {
						if (((this.Keys = []), (this.Values = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Keys = c.emptyArray),
						(e.prototype.Values = c.emptyArray),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if ((t || (t = u.create()), null != e.Keys && e.Keys.length))
								for (var n = 0; n < e.Keys.length; ++n)
									t.uint32(10).string(e.Keys[n]);
							if (null != e.Values && e.Values.length)
								for (n = 0; n < e.Values.length; ++n)
									t.uint32(18).string(e.Values[n]);
							return t;
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsConf();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										(r.Keys && r.Keys.length) || (r.Keys = []),
											r.Keys.push(e.string());
										break;
									case 2:
										(r.Values && r.Values.length) || (r.Values = []),
											r.Values.push(e.string());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.Keys && e.hasOwnProperty("Keys")) {
								if (!Array.isArray(e.Keys)) return "Keys: array expected";
								for (var t = 0; t < e.Keys.length; ++t)
									if (!c.isString(e.Keys[t])) return "Keys: string[] expected";
							}
							if (null != e.Values && e.hasOwnProperty("Values")) {
								if (!Array.isArray(e.Values)) return "Values: array expected";
								for (t = 0; t < e.Values.length; ++t)
									if (!c.isString(e.Values[t]))
										return "Values: string[] expected";
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsConf) return e;
							var t = new l.manager.ArgumentsConf();
							if (e.Keys) {
								if (!Array.isArray(e.Keys))
									throw TypeError(
										".manager.ArgumentsConf.Keys: array expected"
									);
								t.Keys = [];
								for (var n = 0; n < e.Keys.length; ++n)
									t.Keys[n] = String(e.Keys[n]);
							}
							if (e.Values) {
								if (!Array.isArray(e.Values))
									throw TypeError(
										".manager.ArgumentsConf.Values: array expected"
									);
								for (t.Values = [], n = 0; n < e.Values.length; ++n)
									t.Values[n] = String(e.Values[n]);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && ((n.Keys = []), (n.Values = [])),
								e.Keys && e.Keys.length)
							) {
								n.Keys = [];
								for (var r = 0; r < e.Keys.length; ++r) n.Keys[r] = e.Keys[r];
							}
							if (e.Values && e.Values.length)
								for (n.Values = [], r = 0; r < e.Values.length; ++r)
									n.Values[r] = e.Values[r];
							return n;
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.SwarmChangeReason = (function () {
					var e = {},
						t = Object.create(e);
					return (
						(t[(e[0] = "CONNECTED")] = 0),
						(t[(e[1] = "DISCONNECTED")] = 1),
						(t[(e[2] = "CONNECTERR")] = 2),
						(t[(e[3] = "CHANNELSWITCH")] = 3),
						(t[(e[4] = "PINGPONG")] = 4),
						t
					);
				})()),
				(o.ArgumentsEvent = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					var t;
					return (
						(e.prototype.EventName = 0),
						(e.prototype.Action = 0),
						(e.prototype.PeerID = ""),
						(e.prototype.RemotePeerID = ""),
						(e.prototype.ArgumentsP2PPart = null),
						(e.prototype.ArgumentsP2PReq = null),
						(e.prototype.ArgumentsP2PStats = null),
						(e.prototype.ArgumentsPeerInfo = null),
						(e.prototype.ArgumentsPeerVisit = null),
						(e.prototype.ArgumentsRegistered = null),
						(e.prototype.ArgumentsResourceDownloaded = null),
						(e.prototype.ArgumentsResourceExchanges = null),
						(e.prototype.ArgumentsResourceUploaded = null),
						(e.prototype.ArgumentsPlayerInfo = null),
						(e.prototype.ArgumentsSwarmSizeUpdate = null),
						(e.prototype.ArgumentsSlotUpdate = null),
						(e.prototype.ArgumentsConf = null),
						(e.prototype.ArgumentsPeerState = null),
						(e.prototype.ArgumentsPlayerState = null),
						(e.prototype.ArgumentsNetworkInfo = null),
						(e.prototype.ArgumentsPingPongExchange = null),
						(e.prototype.ArgumentsResourceAvailability = null),
						(e.prototype.ArgumentsAvgDelay = null),
						(e.prototype.ArgumentsDeviceState = null),
						Object.defineProperty(e.prototype, "Additional", {
							get: c.oneOfGetter(
								(t = [
									"ArgumentsP2PPart",
									"ArgumentsP2PReq",
									"ArgumentsP2PStats",
									"ArgumentsPeerInfo",
									"ArgumentsPeerVisit",
									"ArgumentsRegistered",
									"ArgumentsResourceDownloaded",
									"ArgumentsResourceExchanges",
									"ArgumentsResourceUploaded",
									"ArgumentsPlayerInfo",
									"ArgumentsSwarmSizeUpdate",
									"ArgumentsSlotUpdate",
									"ArgumentsConf",
									"ArgumentsPeerState",
									"ArgumentsPlayerState",
									"ArgumentsNetworkInfo",
									"ArgumentsPingPongExchange",
									"ArgumentsResourceAvailability",
									"ArgumentsAvgDelay",
									"ArgumentsDeviceState",
								])
							),
							set: c.oneOfSetter(t),
						}),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.EventName &&
									e.hasOwnProperty("EventName") &&
									t.uint32(8).int32(e.EventName),
								null != e.Action &&
									e.hasOwnProperty("Action") &&
									t.uint32(16).int32(e.Action),
								null != e.PeerID &&
									e.hasOwnProperty("PeerID") &&
									t.uint32(26).string(e.PeerID),
								null != e.RemotePeerID &&
									e.hasOwnProperty("RemotePeerID") &&
									t.uint32(34).string(e.RemotePeerID),
								null != e.ArgumentsP2PPart &&
									e.hasOwnProperty("ArgumentsP2PPart") &&
									l.manager.ArgumentsP2PPart.encode(
										e.ArgumentsP2PPart,
										t.uint32(42).fork()
									).ldelim(),
								null != e.ArgumentsP2PReq &&
									e.hasOwnProperty("ArgumentsP2PReq") &&
									l.manager.ArgumentsP2PReq.encode(
										e.ArgumentsP2PReq,
										t.uint32(50).fork()
									).ldelim(),
								null != e.ArgumentsPeerInfo &&
									e.hasOwnProperty("ArgumentsPeerInfo") &&
									l.manager.ArgumentsPeerInfo.encode(
										e.ArgumentsPeerInfo,
										t.uint32(58).fork()
									).ldelim(),
								null != e.ArgumentsP2PStats &&
									e.hasOwnProperty("ArgumentsP2PStats") &&
									l.manager.PeeringStats.encode(
										e.ArgumentsP2PStats,
										t.uint32(66).fork()
									).ldelim(),
								null != e.ArgumentsRegistered &&
									e.hasOwnProperty("ArgumentsRegistered") &&
									l.manager.ArgumentsRegistered.encode(
										e.ArgumentsRegistered,
										t.uint32(74).fork()
									).ldelim(),
								null != e.ArgumentsPeerVisit &&
									e.hasOwnProperty("ArgumentsPeerVisit") &&
									l.manager.PeerVisit.encode(
										e.ArgumentsPeerVisit,
										t.uint32(82).fork()
									).ldelim(),
								null != e.ArgumentsResourceDownloaded &&
									e.hasOwnProperty("ArgumentsResourceDownloaded") &&
									l.manager.ResourceExchanges.encode(
										e.ArgumentsResourceDownloaded,
										t.uint32(90).fork()
									).ldelim(),
								null != e.ArgumentsPlayerInfo &&
									e.hasOwnProperty("ArgumentsPlayerInfo") &&
									l.manager.ArgumentsPlayerInfo.encode(
										e.ArgumentsPlayerInfo,
										t.uint32(98).fork()
									).ldelim(),
								null != e.ArgumentsResourceUploaded &&
									e.hasOwnProperty("ArgumentsResourceUploaded") &&
									l.manager.ResourceExchanges.encode(
										e.ArgumentsResourceUploaded,
										t.uint32(106).fork()
									).ldelim(),
								null != e.ArgumentsSwarmSizeUpdate &&
									e.hasOwnProperty("ArgumentsSwarmSizeUpdate") &&
									l.manager.ArgumentsSwarmSizeUpdate.encode(
										e.ArgumentsSwarmSizeUpdate,
										t.uint32(114).fork()
									).ldelim(),
								null != e.ArgumentsSlotUpdate &&
									e.hasOwnProperty("ArgumentsSlotUpdate") &&
									l.manager.SlotInfo.encode(
										e.ArgumentsSlotUpdate,
										t.uint32(122).fork()
									).ldelim(),
								null != e.ArgumentsConf &&
									e.hasOwnProperty("ArgumentsConf") &&
									l.manager.ArgumentsConf.encode(
										e.ArgumentsConf,
										t.uint32(130).fork()
									).ldelim(),
								null != e.ArgumentsPeerState &&
									e.hasOwnProperty("ArgumentsPeerState") &&
									l.manager.PeerState.encode(
										e.ArgumentsPeerState,
										t.uint32(138).fork()
									).ldelim(),
								null != e.ArgumentsPlayerState &&
									e.hasOwnProperty("ArgumentsPlayerState") &&
									l.manager.PlayerState.encode(
										e.ArgumentsPlayerState,
										t.uint32(146).fork()
									).ldelim(),
								null != e.ArgumentsNetworkInfo &&
									e.hasOwnProperty("ArgumentsNetworkInfo") &&
									l.manager.NetworkInfo.encode(
										e.ArgumentsNetworkInfo,
										t.uint32(154).fork()
									).ldelim(),
								null != e.ArgumentsPingPongExchange &&
									e.hasOwnProperty("ArgumentsPingPongExchange") &&
									l.manager.PingPongExchange.encode(
										e.ArgumentsPingPongExchange,
										t.uint32(162).fork()
									).ldelim(),
								null != e.ArgumentsResourceAvailability &&
									e.hasOwnProperty("ArgumentsResourceAvailability") &&
									l.manager.ResourceAvailability.encode(
										e.ArgumentsResourceAvailability,
										t.uint32(170).fork()
									).ldelim(),
								null != e.ArgumentsAvgDelay &&
									e.hasOwnProperty("ArgumentsAvgDelay") &&
									l.manager.PingPongDelay.encode(
										e.ArgumentsAvgDelay,
										t.uint32(178).fork()
									).ldelim(),
								null != e.ArgumentsDeviceState &&
									e.hasOwnProperty("ArgumentsDeviceState") &&
									l.manager.ArgumentsDeviceState.encode(
										e.ArgumentsDeviceState,
										t.uint32(186).fork()
									).ldelim(),
								null != e.ArgumentsResourceExchanges &&
									e.hasOwnProperty("ArgumentsResourceExchanges") &&
									l.manager.ArgumentsResourceExchanges.encode(
										e.ArgumentsResourceExchanges,
										t.uint32(890).fork()
									).ldelim(),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsEvent();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.EventName = e.int32();
										break;
									case 2:
										r.Action = e.int32();
										break;
									case 3:
										r.PeerID = e.string();
										break;
									case 4:
										r.RemotePeerID = e.string();
										break;
									case 5:
										r.ArgumentsP2PPart = l.manager.ArgumentsP2PPart.decode(
											e,
											e.uint32()
										);
										break;
									case 6:
										r.ArgumentsP2PReq = l.manager.ArgumentsP2PReq.decode(
											e,
											e.uint32()
										);
										break;
									case 8:
										r.ArgumentsP2PStats = l.manager.PeeringStats.decode(
											e,
											e.uint32()
										);
										break;
									case 7:
										r.ArgumentsPeerInfo = l.manager.ArgumentsPeerInfo.decode(
											e,
											e.uint32()
										);
										break;
									case 10:
										r.ArgumentsPeerVisit = l.manager.PeerVisit.decode(
											e,
											e.uint32()
										);
										break;
									case 9:
										r.ArgumentsRegistered =
											l.manager.ArgumentsRegistered.decode(e, e.uint32());
										break;
									case 11:
										r.ArgumentsResourceDownloaded =
											l.manager.ResourceExchanges.decode(e, e.uint32());
										break;
									case 111:
										r.ArgumentsResourceExchanges =
											l.manager.ArgumentsResourceExchanges.decode(
												e,
												e.uint32()
											);
										break;
									case 13:
										r.ArgumentsResourceUploaded =
											l.manager.ResourceExchanges.decode(e, e.uint32());
										break;
									case 12:
										r.ArgumentsPlayerInfo =
											l.manager.ArgumentsPlayerInfo.decode(e, e.uint32());
										break;
									case 14:
										r.ArgumentsSwarmSizeUpdate =
											l.manager.ArgumentsSwarmSizeUpdate.decode(e, e.uint32());
										break;
									case 15:
										r.ArgumentsSlotUpdate = l.manager.SlotInfo.decode(
											e,
											e.uint32()
										);
										break;
									case 16:
										r.ArgumentsConf = l.manager.ArgumentsConf.decode(
											e,
											e.uint32()
										);
										break;
									case 17:
										r.ArgumentsPeerState = l.manager.PeerState.decode(
											e,
											e.uint32()
										);
										break;
									case 18:
										r.ArgumentsPlayerState = l.manager.PlayerState.decode(
											e,
											e.uint32()
										);
										break;
									case 19:
										r.ArgumentsNetworkInfo = l.manager.NetworkInfo.decode(
											e,
											e.uint32()
										);
										break;
									case 20:
										r.ArgumentsPingPongExchange =
											l.manager.PingPongExchange.decode(e, e.uint32());
										break;
									case 21:
										r.ArgumentsResourceAvailability =
											l.manager.ResourceAvailability.decode(e, e.uint32());
										break;
									case 22:
										r.ArgumentsAvgDelay = l.manager.PingPongDelay.decode(
											e,
											e.uint32()
										);
										break;
									case 23:
										r.ArgumentsDeviceState =
											l.manager.ArgumentsDeviceState.decode(e, e.uint32());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							var t = {};
							if (null != e.EventName && e.hasOwnProperty("EventName"))
								switch (e.EventName) {
									default:
										return "EventName: enum value expected";
									case 0:
									case 1:
									case 2:
									case 3:
									case 4:
									case 5:
									case 6:
									case 7:
									case 8:
									case 10:
								}
							if (null != e.Action && e.hasOwnProperty("Action"))
								switch (e.Action) {
									default:
										return "Action: enum value expected";
									case 0:
									case 1:
									case 2:
									case 10:
									case 11:
									case 13:
									case 14:
									case 141:
									case 12:
									case 121:
									case 15:
									case 16:
									case 17:
									case 18:
									case 19:
									case 20:
									case 201:
									case 202:
									case 203:
									case 21:
									case 22:
									case 23:
									case 24:
									case 211:
									case 25:
									case 26:
								}
							if (
								null != e.PeerID &&
								e.hasOwnProperty("PeerID") &&
								!c.isString(e.PeerID)
							)
								return "PeerID: string expected";
							if (
								null != e.RemotePeerID &&
								e.hasOwnProperty("RemotePeerID") &&
								!c.isString(e.RemotePeerID)
							)
								return "RemotePeerID: string expected";
							if (
								null != e.ArgumentsP2PPart &&
								e.hasOwnProperty("ArgumentsP2PPart") &&
								((t.Additional = 1),
								(n = l.manager.ArgumentsP2PPart.verify(e.ArgumentsP2PPart)))
							)
								return "ArgumentsP2PPart." + n;
							if (
								null != e.ArgumentsP2PReq &&
								e.hasOwnProperty("ArgumentsP2PReq")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsP2PReq.verify(e.ArgumentsP2PReq)))
								)
									return "ArgumentsP2PReq." + n;
							}
							if (
								null != e.ArgumentsP2PStats &&
								e.hasOwnProperty("ArgumentsP2PStats")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.PeeringStats.verify(e.ArgumentsP2PStats)))
								)
									return "ArgumentsP2PStats." + n;
							}
							if (
								null != e.ArgumentsPeerInfo &&
								e.hasOwnProperty("ArgumentsPeerInfo")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsPeerInfo.verify(e.ArgumentsPeerInfo)))
								)
									return "ArgumentsPeerInfo." + n;
							}
							if (
								null != e.ArgumentsPeerVisit &&
								e.hasOwnProperty("ArgumentsPeerVisit")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.PeerVisit.verify(e.ArgumentsPeerVisit)))
								)
									return "ArgumentsPeerVisit." + n;
							}
							if (
								null != e.ArgumentsRegistered &&
								e.hasOwnProperty("ArgumentsRegistered")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsRegistered.verify(
										e.ArgumentsRegistered
									)))
								)
									return "ArgumentsRegistered." + n;
							}
							if (
								null != e.ArgumentsResourceDownloaded &&
								e.hasOwnProperty("ArgumentsResourceDownloaded")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ResourceExchanges.verify(
										e.ArgumentsResourceDownloaded
									)))
								)
									return "ArgumentsResourceDownloaded." + n;
							}
							if (
								null != e.ArgumentsResourceExchanges &&
								e.hasOwnProperty("ArgumentsResourceExchanges")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsResourceExchanges.verify(
										e.ArgumentsResourceExchanges
									)))
								)
									return "ArgumentsResourceExchanges." + n;
							}
							if (
								null != e.ArgumentsResourceUploaded &&
								e.hasOwnProperty("ArgumentsResourceUploaded")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ResourceExchanges.verify(
										e.ArgumentsResourceUploaded
									)))
								)
									return "ArgumentsResourceUploaded." + n;
							}
							if (
								null != e.ArgumentsPlayerInfo &&
								e.hasOwnProperty("ArgumentsPlayerInfo")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsPlayerInfo.verify(
										e.ArgumentsPlayerInfo
									)))
								)
									return "ArgumentsPlayerInfo." + n;
							}
							if (
								null != e.ArgumentsSwarmSizeUpdate &&
								e.hasOwnProperty("ArgumentsSwarmSizeUpdate")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsSwarmSizeUpdate.verify(
										e.ArgumentsSwarmSizeUpdate
									)))
								)
									return "ArgumentsSwarmSizeUpdate." + n;
							}
							if (
								null != e.ArgumentsSlotUpdate &&
								e.hasOwnProperty("ArgumentsSlotUpdate")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.SlotInfo.verify(e.ArgumentsSlotUpdate)))
								)
									return "ArgumentsSlotUpdate." + n;
							}
							if (
								null != e.ArgumentsConf &&
								e.hasOwnProperty("ArgumentsConf")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsConf.verify(e.ArgumentsConf)))
								)
									return "ArgumentsConf." + n;
							}
							if (
								null != e.ArgumentsPeerState &&
								e.hasOwnProperty("ArgumentsPeerState")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.PeerState.verify(e.ArgumentsPeerState)))
								)
									return "ArgumentsPeerState." + n;
							}
							if (
								null != e.ArgumentsPlayerState &&
								e.hasOwnProperty("ArgumentsPlayerState")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.PlayerState.verify(e.ArgumentsPlayerState)))
								)
									return "ArgumentsPlayerState." + n;
							}
							if (
								null != e.ArgumentsNetworkInfo &&
								e.hasOwnProperty("ArgumentsNetworkInfo")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.NetworkInfo.verify(e.ArgumentsNetworkInfo)))
								)
									return "ArgumentsNetworkInfo." + n;
							}
							if (
								null != e.ArgumentsPingPongExchange &&
								e.hasOwnProperty("ArgumentsPingPongExchange")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.PingPongExchange.verify(
										e.ArgumentsPingPongExchange
									)))
								)
									return "ArgumentsPingPongExchange." + n;
							}
							if (
								null != e.ArgumentsResourceAvailability &&
								e.hasOwnProperty("ArgumentsResourceAvailability")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.ResourceAvailability.verify(
										e.ArgumentsResourceAvailability
									)))
								)
									return "ArgumentsResourceAvailability." + n;
							}
							if (
								null != e.ArgumentsAvgDelay &&
								e.hasOwnProperty("ArgumentsAvgDelay")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								if (
									((t.Additional = 1),
									(n = l.manager.PingPongDelay.verify(e.ArgumentsAvgDelay)))
								)
									return "ArgumentsAvgDelay." + n;
							}
							if (
								null != e.ArgumentsDeviceState &&
								e.hasOwnProperty("ArgumentsDeviceState")
							) {
								if (1 === t.Additional) return "Additional: multiple values";
								var n;
								if (
									((t.Additional = 1),
									(n = l.manager.ArgumentsDeviceState.verify(
										e.ArgumentsDeviceState
									)))
								)
									return "ArgumentsDeviceState." + n;
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsEvent) return e;
							var t = new l.manager.ArgumentsEvent();
							switch (e.EventName) {
								case "RTC":
								case 0:
									t.EventName = 0;
									break;
								case "PEER":
								case 1:
									t.EventName = 1;
									break;
								case "RESOURCE":
								case 2:
									t.EventName = 2;
									break;
								case "PLAYER":
								case 3:
									t.EventName = 3;
									break;
								case "P2P":
								case 4:
									t.EventName = 4;
									break;
								case "SWARM":
								case 5:
									t.EventName = 5;
									break;
								case "LIB":
								case 6:
									t.EventName = 6;
									break;
								case "NETWORK":
								case 7:
									t.EventName = 7;
									break;
								case "PINGPONG":
								case 8:
									t.EventName = 8;
									break;
								case "DEVICESTATE":
								case 10:
									t.EventName = 10;
							}
							switch (e.Action) {
								case "INIT":
								case 0:
									t.Action = 0;
									break;
								case "OPEN":
								case 1:
									t.Action = 1;
									break;
								case "CLOSE":
								case 2:
									t.Action = 2;
									break;
								case "SEND":
								case 10:
									t.Action = 10;
									break;
								case "RCVD":
								case 11:
									t.Action = 11;
									break;
								case "BUSY":
								case 13:
									t.Action = 13;
									break;
								case "REQUEST":
								case 14:
									t.Action = 14;
									break;
								case "STATS":
								case 141:
									t.Action = 141;
									break;
								case "DOWNLOADED":
								case 12:
									t.Action = 12;
									break;
								case "EXCHANGE":
								case 121:
									t.Action = 121;
									break;
								case "UPLOADED":
								case 15:
									t.Action = 15;
									break;
								case "SLOTUPDATE":
								case 16:
									t.Action = 16;
									break;
								case "STORAGE":
								case 17:
									t.Action = 17;
									break;
								case "AVAILABILITY":
								case 18:
									t.Action = 18;
									break;
								case "DELAY":
								case 19:
									t.Action = 19;
									break;
								case "INFO":
								case 20:
									t.Action = 20;
									break;
								case "REGISTERED":
								case 201:
									t.Action = 201;
									break;
								case "VISIT":
								case 202:
									t.Action = 202;
									break;
								case "STATE":
								case 203:
									t.Action = 203;
									break;
								case "PLAY":
								case 21:
									t.Action = 21;
									break;
								case "PAUSE":
								case 22:
									t.Action = 22;
									break;
								case "REBUFFER":
								case 23:
									t.Action = 23;
									break;
								case "STOP":
								case 24:
									t.Action = 24;
									break;
								case "FLUCTUATE":
								case 211:
									t.Action = 211;
									break;
								case "SIZEUPDATE":
								case 25:
									t.Action = 25;
									break;
								case "CONF":
								case 26:
									t.Action = 26;
							}
							if (
								(null != e.PeerID && (t.PeerID = String(e.PeerID)),
								null != e.RemotePeerID &&
									(t.RemotePeerID = String(e.RemotePeerID)),
								null != e.ArgumentsP2PPart)
							) {
								if ("object" != typeof e.ArgumentsP2PPart)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsP2PPart: object expected"
									);
								t.ArgumentsP2PPart = l.manager.ArgumentsP2PPart.fromObject(
									e.ArgumentsP2PPart
								);
							}
							if (null != e.ArgumentsP2PReq) {
								if ("object" != typeof e.ArgumentsP2PReq)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsP2PReq: object expected"
									);
								t.ArgumentsP2PReq = l.manager.ArgumentsP2PReq.fromObject(
									e.ArgumentsP2PReq
								);
							}
							if (null != e.ArgumentsP2PStats) {
								if ("object" != typeof e.ArgumentsP2PStats)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsP2PStats: object expected"
									);
								t.ArgumentsP2PStats = l.manager.PeeringStats.fromObject(
									e.ArgumentsP2PStats
								);
							}
							if (null != e.ArgumentsPeerInfo) {
								if ("object" != typeof e.ArgumentsPeerInfo)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsPeerInfo: object expected"
									);
								t.ArgumentsPeerInfo = l.manager.ArgumentsPeerInfo.fromObject(
									e.ArgumentsPeerInfo
								);
							}
							if (null != e.ArgumentsPeerVisit) {
								if ("object" != typeof e.ArgumentsPeerVisit)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsPeerVisit: object expected"
									);
								t.ArgumentsPeerVisit = l.manager.PeerVisit.fromObject(
									e.ArgumentsPeerVisit
								);
							}
							if (null != e.ArgumentsRegistered) {
								if ("object" != typeof e.ArgumentsRegistered)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsRegistered: object expected"
									);
								t.ArgumentsRegistered =
									l.manager.ArgumentsRegistered.fromObject(
										e.ArgumentsRegistered
									);
							}
							if (null != e.ArgumentsResourceDownloaded) {
								if ("object" != typeof e.ArgumentsResourceDownloaded)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsResourceDownloaded: object expected"
									);
								t.ArgumentsResourceDownloaded =
									l.manager.ResourceExchanges.fromObject(
										e.ArgumentsResourceDownloaded
									);
							}
							if (null != e.ArgumentsResourceExchanges) {
								if ("object" != typeof e.ArgumentsResourceExchanges)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsResourceExchanges: object expected"
									);
								t.ArgumentsResourceExchanges =
									l.manager.ArgumentsResourceExchanges.fromObject(
										e.ArgumentsResourceExchanges
									);
							}
							if (null != e.ArgumentsResourceUploaded) {
								if ("object" != typeof e.ArgumentsResourceUploaded)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsResourceUploaded: object expected"
									);
								t.ArgumentsResourceUploaded =
									l.manager.ResourceExchanges.fromObject(
										e.ArgumentsResourceUploaded
									);
							}
							if (null != e.ArgumentsPlayerInfo) {
								if ("object" != typeof e.ArgumentsPlayerInfo)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsPlayerInfo: object expected"
									);
								t.ArgumentsPlayerInfo =
									l.manager.ArgumentsPlayerInfo.fromObject(
										e.ArgumentsPlayerInfo
									);
							}
							if (null != e.ArgumentsSwarmSizeUpdate) {
								if ("object" != typeof e.ArgumentsSwarmSizeUpdate)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsSwarmSizeUpdate: object expected"
									);
								t.ArgumentsSwarmSizeUpdate =
									l.manager.ArgumentsSwarmSizeUpdate.fromObject(
										e.ArgumentsSwarmSizeUpdate
									);
							}
							if (null != e.ArgumentsSlotUpdate) {
								if ("object" != typeof e.ArgumentsSlotUpdate)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsSlotUpdate: object expected"
									);
								t.ArgumentsSlotUpdate = l.manager.SlotInfo.fromObject(
									e.ArgumentsSlotUpdate
								);
							}
							if (null != e.ArgumentsConf) {
								if ("object" != typeof e.ArgumentsConf)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsConf: object expected"
									);
								t.ArgumentsConf = l.manager.ArgumentsConf.fromObject(
									e.ArgumentsConf
								);
							}
							if (null != e.ArgumentsPeerState) {
								if ("object" != typeof e.ArgumentsPeerState)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsPeerState: object expected"
									);
								t.ArgumentsPeerState = l.manager.PeerState.fromObject(
									e.ArgumentsPeerState
								);
							}
							if (null != e.ArgumentsPlayerState) {
								if ("object" != typeof e.ArgumentsPlayerState)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsPlayerState: object expected"
									);
								t.ArgumentsPlayerState = l.manager.PlayerState.fromObject(
									e.ArgumentsPlayerState
								);
							}
							if (null != e.ArgumentsNetworkInfo) {
								if ("object" != typeof e.ArgumentsNetworkInfo)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsNetworkInfo: object expected"
									);
								t.ArgumentsNetworkInfo = l.manager.NetworkInfo.fromObject(
									e.ArgumentsNetworkInfo
								);
							}
							if (null != e.ArgumentsPingPongExchange) {
								if ("object" != typeof e.ArgumentsPingPongExchange)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsPingPongExchange: object expected"
									);
								t.ArgumentsPingPongExchange =
									l.manager.PingPongExchange.fromObject(
										e.ArgumentsPingPongExchange
									);
							}
							if (null != e.ArgumentsResourceAvailability) {
								if ("object" != typeof e.ArgumentsResourceAvailability)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsResourceAvailability: object expected"
									);
								t.ArgumentsResourceAvailability =
									l.manager.ResourceAvailability.fromObject(
										e.ArgumentsResourceAvailability
									);
							}
							if (null != e.ArgumentsAvgDelay) {
								if ("object" != typeof e.ArgumentsAvgDelay)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsAvgDelay: object expected"
									);
								t.ArgumentsAvgDelay = l.manager.PingPongDelay.fromObject(
									e.ArgumentsAvgDelay
								);
							}
							if (null != e.ArgumentsDeviceState) {
								if ("object" != typeof e.ArgumentsDeviceState)
									throw TypeError(
										".manager.ArgumentsEvent.ArgumentsDeviceState: object expected"
									);
								t.ArgumentsDeviceState =
									l.manager.ArgumentsDeviceState.fromObject(
										e.ArgumentsDeviceState
									);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.EventName = t.enums === String ? "RTC" : 0),
									(n.Action = t.enums === String ? "INIT" : 0),
									(n.PeerID = ""),
									(n.RemotePeerID = "")),
								null != e.EventName &&
									e.hasOwnProperty("EventName") &&
									(n.EventName =
										t.enums === String
											? l.manager.ArgumentsEvent.EventClass[e.EventName]
											: e.EventName),
								null != e.Action &&
									e.hasOwnProperty("Action") &&
									(n.Action =
										t.enums === String
											? l.manager.ArgumentsEvent.Actions[e.Action]
											: e.Action),
								null != e.PeerID &&
									e.hasOwnProperty("PeerID") &&
									(n.PeerID = e.PeerID),
								null != e.RemotePeerID &&
									e.hasOwnProperty("RemotePeerID") &&
									(n.RemotePeerID = e.RemotePeerID),
								null != e.ArgumentsP2PPart &&
									e.hasOwnProperty("ArgumentsP2PPart") &&
									((n.ArgumentsP2PPart = l.manager.ArgumentsP2PPart.toObject(
										e.ArgumentsP2PPart,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsP2PPart")),
								null != e.ArgumentsP2PReq &&
									e.hasOwnProperty("ArgumentsP2PReq") &&
									((n.ArgumentsP2PReq = l.manager.ArgumentsP2PReq.toObject(
										e.ArgumentsP2PReq,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsP2PReq")),
								null != e.ArgumentsPeerInfo &&
									e.hasOwnProperty("ArgumentsPeerInfo") &&
									((n.ArgumentsPeerInfo = l.manager.ArgumentsPeerInfo.toObject(
										e.ArgumentsPeerInfo,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsPeerInfo")),
								null != e.ArgumentsP2PStats &&
									e.hasOwnProperty("ArgumentsP2PStats") &&
									((n.ArgumentsP2PStats = l.manager.PeeringStats.toObject(
										e.ArgumentsP2PStats,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsP2PStats")),
								null != e.ArgumentsRegistered &&
									e.hasOwnProperty("ArgumentsRegistered") &&
									((n.ArgumentsRegistered =
										l.manager.ArgumentsRegistered.toObject(
											e.ArgumentsRegistered,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsRegistered")),
								null != e.ArgumentsPeerVisit &&
									e.hasOwnProperty("ArgumentsPeerVisit") &&
									((n.ArgumentsPeerVisit = l.manager.PeerVisit.toObject(
										e.ArgumentsPeerVisit,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsPeerVisit")),
								null != e.ArgumentsResourceDownloaded &&
									e.hasOwnProperty("ArgumentsResourceDownloaded") &&
									((n.ArgumentsResourceDownloaded =
										l.manager.ResourceExchanges.toObject(
											e.ArgumentsResourceDownloaded,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsResourceDownloaded")),
								null != e.ArgumentsPlayerInfo &&
									e.hasOwnProperty("ArgumentsPlayerInfo") &&
									((n.ArgumentsPlayerInfo =
										l.manager.ArgumentsPlayerInfo.toObject(
											e.ArgumentsPlayerInfo,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsPlayerInfo")),
								null != e.ArgumentsResourceUploaded &&
									e.hasOwnProperty("ArgumentsResourceUploaded") &&
									((n.ArgumentsResourceUploaded =
										l.manager.ResourceExchanges.toObject(
											e.ArgumentsResourceUploaded,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsResourceUploaded")),
								null != e.ArgumentsSwarmSizeUpdate &&
									e.hasOwnProperty("ArgumentsSwarmSizeUpdate") &&
									((n.ArgumentsSwarmSizeUpdate =
										l.manager.ArgumentsSwarmSizeUpdate.toObject(
											e.ArgumentsSwarmSizeUpdate,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsSwarmSizeUpdate")),
								null != e.ArgumentsSlotUpdate &&
									e.hasOwnProperty("ArgumentsSlotUpdate") &&
									((n.ArgumentsSlotUpdate = l.manager.SlotInfo.toObject(
										e.ArgumentsSlotUpdate,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsSlotUpdate")),
								null != e.ArgumentsConf &&
									e.hasOwnProperty("ArgumentsConf") &&
									((n.ArgumentsConf = l.manager.ArgumentsConf.toObject(
										e.ArgumentsConf,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsConf")),
								null != e.ArgumentsPeerState &&
									e.hasOwnProperty("ArgumentsPeerState") &&
									((n.ArgumentsPeerState = l.manager.PeerState.toObject(
										e.ArgumentsPeerState,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsPeerState")),
								null != e.ArgumentsPlayerState &&
									e.hasOwnProperty("ArgumentsPlayerState") &&
									((n.ArgumentsPlayerState = l.manager.PlayerState.toObject(
										e.ArgumentsPlayerState,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsPlayerState")),
								null != e.ArgumentsNetworkInfo &&
									e.hasOwnProperty("ArgumentsNetworkInfo") &&
									((n.ArgumentsNetworkInfo = l.manager.NetworkInfo.toObject(
										e.ArgumentsNetworkInfo,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsNetworkInfo")),
								null != e.ArgumentsPingPongExchange &&
									e.hasOwnProperty("ArgumentsPingPongExchange") &&
									((n.ArgumentsPingPongExchange =
										l.manager.PingPongExchange.toObject(
											e.ArgumentsPingPongExchange,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsPingPongExchange")),
								null != e.ArgumentsResourceAvailability &&
									e.hasOwnProperty("ArgumentsResourceAvailability") &&
									((n.ArgumentsResourceAvailability =
										l.manager.ResourceAvailability.toObject(
											e.ArgumentsResourceAvailability,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsResourceAvailability")),
								null != e.ArgumentsAvgDelay &&
									e.hasOwnProperty("ArgumentsAvgDelay") &&
									((n.ArgumentsAvgDelay = l.manager.PingPongDelay.toObject(
										e.ArgumentsAvgDelay,
										t
									)),
									t.oneofs && (n.Additional = "ArgumentsAvgDelay")),
								null != e.ArgumentsDeviceState &&
									e.hasOwnProperty("ArgumentsDeviceState") &&
									((n.ArgumentsDeviceState =
										l.manager.ArgumentsDeviceState.toObject(
											e.ArgumentsDeviceState,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsDeviceState")),
								null != e.ArgumentsResourceExchanges &&
									e.hasOwnProperty("ArgumentsResourceExchanges") &&
									((n.ArgumentsResourceExchanges =
										l.manager.ArgumentsResourceExchanges.toObject(
											e.ArgumentsResourceExchanges,
											t
										)),
									t.oneofs && (n.Additional = "ArgumentsResourceExchanges")),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						(e.EventClass = (function () {
							var e = {},
								t = Object.create(e);
							return (
								(t[(e[0] = "RTC")] = 0),
								(t[(e[1] = "PEER")] = 1),
								(t[(e[2] = "RESOURCE")] = 2),
								(t[(e[3] = "PLAYER")] = 3),
								(t[(e[4] = "P2P")] = 4),
								(t[(e[5] = "SWARM")] = 5),
								(t[(e[6] = "LIB")] = 6),
								(t[(e[7] = "NETWORK")] = 7),
								(t[(e[8] = "PINGPONG")] = 8),
								(t[(e[10] = "DEVICESTATE")] = 10),
								t
							);
						})()),
						(e.Actions = (function () {
							var e = {},
								t = Object.create(e);
							return (
								(t[(e[0] = "INIT")] = 0),
								(t[(e[1] = "OPEN")] = 1),
								(t[(e[2] = "CLOSE")] = 2),
								(t[(e[10] = "SEND")] = 10),
								(t[(e[11] = "RCVD")] = 11),
								(t[(e[13] = "BUSY")] = 13),
								(t[(e[14] = "REQUEST")] = 14),
								(t[(e[141] = "STATS")] = 141),
								(t[(e[12] = "DOWNLOADED")] = 12),
								(t[(e[121] = "EXCHANGE")] = 121),
								(t[(e[15] = "UPLOADED")] = 15),
								(t[(e[16] = "SLOTUPDATE")] = 16),
								(t[(e[17] = "STORAGE")] = 17),
								(t[(e[18] = "AVAILABILITY")] = 18),
								(t[(e[19] = "DELAY")] = 19),
								(t[(e[20] = "INFO")] = 20),
								(t[(e[201] = "REGISTERED")] = 201),
								(t[(e[202] = "VISIT")] = 202),
								(t[(e[203] = "STATE")] = 203),
								(t[(e[21] = "PLAY")] = 21),
								(t[(e[22] = "PAUSE")] = 22),
								(t[(e[23] = "REBUFFER")] = 23),
								(t[(e[24] = "STOP")] = 24),
								(t[(e[211] = "FLUCTUATE")] = 211),
								(t[(e[25] = "SIZEUPDATE")] = 25),
								(t[(e[26] = "CONF")] = 26),
								t
							);
						})()),
						e
					);
				})()),
				(o.ArgumentsP2PReq = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.URL = ""),
						(e.prototype.ToPeerID = ""),
						(e.prototype.Timeout = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.URL &&
									e.hasOwnProperty("URL") &&
									t.uint32(10).string(e.URL),
								null != e.ToPeerID &&
									e.hasOwnProperty("ToPeerID") &&
									t.uint32(18).string(e.ToPeerID),
								null != e.Timeout &&
									e.hasOwnProperty("Timeout") &&
									t.uint32(24).uint32(e.Timeout),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsP2PReq();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.URL = e.string();
										break;
									case 2:
										r.ToPeerID = e.string();
										break;
									case 3:
										r.Timeout = e.uint32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.URL && e.hasOwnProperty("URL") && !c.isString(e.URL)
								? "URL: string expected"
								: null != e.ToPeerID &&
								  e.hasOwnProperty("ToPeerID") &&
								  !c.isString(e.ToPeerID)
								? "ToPeerID: string expected"
								: null != e.Timeout &&
								  e.hasOwnProperty("Timeout") &&
								  !c.isInteger(e.Timeout)
								? "Timeout: integer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsP2PReq) return e;
							var t = new l.manager.ArgumentsP2PReq();
							return (
								null != e.URL && (t.URL = String(e.URL)),
								null != e.ToPeerID && (t.ToPeerID = String(e.ToPeerID)),
								null != e.Timeout && (t.Timeout = e.Timeout >>> 0),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.URL = ""), (n.ToPeerID = ""), (n.Timeout = 0)),
								null != e.URL && e.hasOwnProperty("URL") && (n.URL = e.URL),
								null != e.ToPeerID &&
									e.hasOwnProperty("ToPeerID") &&
									(n.ToPeerID = e.ToPeerID),
								null != e.Timeout &&
									e.hasOwnProperty("Timeout") &&
									(n.Timeout = e.Timeout),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsSwarmSizeUpdate = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Size = 0),
						(e.prototype.Reason = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Size &&
									e.hasOwnProperty("Size") &&
									t.uint32(8).uint32(e.Size),
								null != e.Reason &&
									e.hasOwnProperty("Reason") &&
									t.uint32(16).int32(e.Reason),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsSwarmSizeUpdate();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Size = e.uint32();
										break;
									case 2:
										r.Reason = e.int32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.Size &&
								e.hasOwnProperty("Size") &&
								!c.isInteger(e.Size)
							)
								return "Size: integer expected";
							if (null != e.Reason && e.hasOwnProperty("Reason"))
								switch (e.Reason) {
									default:
										return "Reason: enum value expected";
									case 0:
									case 1:
									case 2:
									case 3:
									case 4:
								}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsSwarmSizeUpdate) return e;
							var t = new l.manager.ArgumentsSwarmSizeUpdate();
							switch ((null != e.Size && (t.Size = e.Size >>> 0), e.Reason)) {
								case "CONNECTED":
								case 0:
									t.Reason = 0;
									break;
								case "DISCONNECTED":
								case 1:
									t.Reason = 1;
									break;
								case "CONNECTERR":
								case 2:
									t.Reason = 2;
									break;
								case "CHANNELSWITCH":
								case 3:
									t.Reason = 3;
									break;
								case "PINGPONG":
								case 4:
									t.Reason = 4;
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.Size = 0),
									(n.Reason = t.enums === String ? "CONNECTED" : 0)),
								null != e.Size && e.hasOwnProperty("Size") && (n.Size = e.Size),
								null != e.Reason &&
									e.hasOwnProperty("Reason") &&
									(n.Reason =
										t.enums === String
											? l.manager.SwarmChangeReason[e.Reason]
											: e.Reason),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.SlotInfo = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.FreeSlot = 0),
						(e.prototype.OccupiedSlot = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.FreeSlot &&
									e.hasOwnProperty("FreeSlot") &&
									t.uint32(8).uint32(e.FreeSlot),
								null != e.OccupiedSlot &&
									e.hasOwnProperty("OccupiedSlot") &&
									t.uint32(16).uint32(e.OccupiedSlot),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.SlotInfo();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.FreeSlot = e.uint32();
										break;
									case 2:
										r.OccupiedSlot = e.uint32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.FreeSlot &&
								  e.hasOwnProperty("FreeSlot") &&
								  !c.isInteger(e.FreeSlot)
								? "FreeSlot: integer expected"
								: null != e.OccupiedSlot &&
								  e.hasOwnProperty("OccupiedSlot") &&
								  !c.isInteger(e.OccupiedSlot)
								? "OccupiedSlot: integer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.SlotInfo) return e;
							var t = new l.manager.SlotInfo();
							return (
								null != e.FreeSlot && (t.FreeSlot = e.FreeSlot >>> 0),
								null != e.OccupiedSlot &&
									(t.OccupiedSlot = e.OccupiedSlot >>> 0),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults && ((n.FreeSlot = 0), (n.OccupiedSlot = 0)),
								null != e.FreeSlot &&
									e.hasOwnProperty("FreeSlot") &&
									(n.FreeSlot = e.FreeSlot),
								null != e.OccupiedSlot &&
									e.hasOwnProperty("OccupiedSlot") &&
									(n.OccupiedSlot = e.OccupiedSlot),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsPeerInfo = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Radio = !1),
						(e.prototype.VOD = !1),
						(e.prototype.OS = ""),
						(e.prototype.Browser = ""),
						(e.prototype.StreamProto = ""),
						(e.prototype.StartUpTime = 0),
						(e.prototype.Content = ""),
						(e.prototype.Origin = ""),
						(e.prototype.Version = ""),
						(e.prototype.Timezone = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Radio &&
									e.hasOwnProperty("Radio") &&
									t.uint32(16).bool(e.Radio),
								null != e.VOD &&
									e.hasOwnProperty("VOD") &&
									t.uint32(24).bool(e.VOD),
								null != e.OS &&
									e.hasOwnProperty("OS") &&
									t.uint32(34).string(e.OS),
								null != e.Browser &&
									e.hasOwnProperty("Browser") &&
									t.uint32(42).string(e.Browser),
								null != e.StreamProto &&
									e.hasOwnProperty("StreamProto") &&
									t.uint32(50).string(e.StreamProto),
								null != e.StartUpTime &&
									e.hasOwnProperty("StartUpTime") &&
									t.uint32(61).float(e.StartUpTime),
								null != e.Content &&
									e.hasOwnProperty("Content") &&
									t.uint32(66).string(e.Content),
								null != e.Origin &&
									e.hasOwnProperty("Origin") &&
									t.uint32(74).string(e.Origin),
								null != e.Version &&
									e.hasOwnProperty("Version") &&
									t.uint32(82).string(e.Version),
								null != e.Timezone &&
									e.hasOwnProperty("Timezone") &&
									t.uint32(88).int64(e.Timezone),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsPeerInfo();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 2:
										r.Radio = e.bool();
										break;
									case 3:
										r.VOD = e.bool();
										break;
									case 4:
										r.OS = e.string();
										break;
									case 5:
										r.Browser = e.string();
										break;
									case 6:
										r.StreamProto = e.string();
										break;
									case 7:
										r.StartUpTime = e.float();
										break;
									case 8:
										r.Content = e.string();
										break;
									case 9:
										r.Origin = e.string();
										break;
									case 10:
										r.Version = e.string();
										break;
									case 11:
										r.Timezone = e.int64();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Radio &&
								  e.hasOwnProperty("Radio") &&
								  "boolean" != typeof e.Radio
								? "Radio: boolean expected"
								: null != e.VOD &&
								  e.hasOwnProperty("VOD") &&
								  "boolean" != typeof e.VOD
								? "VOD: boolean expected"
								: null != e.OS && e.hasOwnProperty("OS") && !c.isString(e.OS)
								? "OS: string expected"
								: null != e.Browser &&
								  e.hasOwnProperty("Browser") &&
								  !c.isString(e.Browser)
								? "Browser: string expected"
								: null != e.StreamProto &&
								  e.hasOwnProperty("StreamProto") &&
								  !c.isString(e.StreamProto)
								? "StreamProto: string expected"
								: null != e.StartUpTime &&
								  e.hasOwnProperty("StartUpTime") &&
								  "number" != typeof e.StartUpTime
								? "StartUpTime: number expected"
								: null != e.Content &&
								  e.hasOwnProperty("Content") &&
								  !c.isString(e.Content)
								? "Content: string expected"
								: null != e.Origin &&
								  e.hasOwnProperty("Origin") &&
								  !c.isString(e.Origin)
								? "Origin: string expected"
								: null != e.Version &&
								  e.hasOwnProperty("Version") &&
								  !c.isString(e.Version)
								? "Version: string expected"
								: null != e.Timezone &&
								  e.hasOwnProperty("Timezone") &&
								  !(
										c.isInteger(e.Timezone) ||
										(e.Timezone &&
											c.isInteger(e.Timezone.low) &&
											c.isInteger(e.Timezone.high))
								  )
								? "Timezone: integer|Long expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsPeerInfo) return e;
							var t = new l.manager.ArgumentsPeerInfo();
							return (
								null != e.Radio && (t.Radio = Boolean(e.Radio)),
								null != e.VOD && (t.VOD = Boolean(e.VOD)),
								null != e.OS && (t.OS = String(e.OS)),
								null != e.Browser && (t.Browser = String(e.Browser)),
								null != e.StreamProto &&
									(t.StreamProto = String(e.StreamProto)),
								null != e.StartUpTime &&
									(t.StartUpTime = Number(e.StartUpTime)),
								null != e.Content && (t.Content = String(e.Content)),
								null != e.Origin && (t.Origin = String(e.Origin)),
								null != e.Version && (t.Version = String(e.Version)),
								null != e.Timezone &&
									(c.Long
										? ((t.Timezone = c.Long.fromValue(e.Timezone)).unsigned =
												!1)
										: "string" == typeof e.Timezone
										? (t.Timezone = parseInt(e.Timezone, 10))
										: "number" == typeof e.Timezone
										? (t.Timezone = e.Timezone)
										: "object" == typeof e.Timezone &&
										  (t.Timezone = new c.LongBits(
												e.Timezone.low >>> 0,
												e.Timezone.high >>> 0
										  ).toNumber())),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults)
								if (
									((n.Radio = !1),
									(n.VOD = !1),
									(n.OS = ""),
									(n.Browser = ""),
									(n.StreamProto = ""),
									(n.StartUpTime = 0),
									(n.Content = ""),
									(n.Origin = ""),
									(n.Version = ""),
									c.Long)
								) {
									var r = new c.Long(0, 0, !1);
									n.Timezone =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Timezone = t.longs === String ? "0" : 0;
							return (
								null != e.Radio &&
									e.hasOwnProperty("Radio") &&
									(n.Radio = e.Radio),
								null != e.VOD && e.hasOwnProperty("VOD") && (n.VOD = e.VOD),
								null != e.OS && e.hasOwnProperty("OS") && (n.OS = e.OS),
								null != e.Browser &&
									e.hasOwnProperty("Browser") &&
									(n.Browser = e.Browser),
								null != e.StreamProto &&
									e.hasOwnProperty("StreamProto") &&
									(n.StreamProto = e.StreamProto),
								null != e.StartUpTime &&
									e.hasOwnProperty("StartUpTime") &&
									(n.StartUpTime =
										t.json && !isFinite(e.StartUpTime)
											? String(e.StartUpTime)
											: e.StartUpTime),
								null != e.Content &&
									e.hasOwnProperty("Content") &&
									(n.Content = e.Content),
								null != e.Origin &&
									e.hasOwnProperty("Origin") &&
									(n.Origin = e.Origin),
								null != e.Version &&
									e.hasOwnProperty("Version") &&
									(n.Version = e.Version),
								null != e.Timezone &&
									e.hasOwnProperty("Timezone") &&
									("number" == typeof e.Timezone
										? (n.Timezone =
												t.longs === String ? String(e.Timezone) : e.Timezone)
										: (n.Timezone =
												t.longs === String
													? c.Long.prototype.toString.call(e.Timezone)
													: t.longs === Number
													? new c.LongBits(
															e.Timezone.low >>> 0,
															e.Timezone.high >>> 0
													  ).toNumber()
													: e.Timezone)),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsP2PPart = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.URL = ""),
						(e.prototype.PartNum = 0),
						(e.prototype.TotalPart = 0),
						(e.prototype.TimeSpent = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.URL &&
									e.hasOwnProperty("URL") &&
									t.uint32(10).string(e.URL),
								null != e.PartNum &&
									e.hasOwnProperty("PartNum") &&
									t.uint32(24).uint32(e.PartNum),
								null != e.TotalPart &&
									e.hasOwnProperty("TotalPart") &&
									t.uint32(32).uint32(e.TotalPart),
								null != e.TimeSpent &&
									e.hasOwnProperty("TimeSpent") &&
									t.uint32(40).uint32(e.TimeSpent),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsP2PPart();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.URL = e.string();
										break;
									case 3:
										r.PartNum = e.uint32();
										break;
									case 4:
										r.TotalPart = e.uint32();
										break;
									case 5:
										r.TimeSpent = e.uint32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.URL && e.hasOwnProperty("URL") && !c.isString(e.URL)
								? "URL: string expected"
								: null != e.PartNum &&
								  e.hasOwnProperty("PartNum") &&
								  !c.isInteger(e.PartNum)
								? "PartNum: integer expected"
								: null != e.TotalPart &&
								  e.hasOwnProperty("TotalPart") &&
								  !c.isInteger(e.TotalPart)
								? "TotalPart: integer expected"
								: null != e.TimeSpent &&
								  e.hasOwnProperty("TimeSpent") &&
								  !c.isInteger(e.TimeSpent)
								? "TimeSpent: integer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsP2PPart) return e;
							var t = new l.manager.ArgumentsP2PPart();
							return (
								null != e.URL && (t.URL = String(e.URL)),
								null != e.PartNum && (t.PartNum = e.PartNum >>> 0),
								null != e.TotalPart && (t.TotalPart = e.TotalPart >>> 0),
								null != e.TimeSpent && (t.TimeSpent = e.TimeSpent >>> 0),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.URL = ""),
									(n.PartNum = 0),
									(n.TotalPart = 0),
									(n.TimeSpent = 0)),
								null != e.URL && e.hasOwnProperty("URL") && (n.URL = e.URL),
								null != e.PartNum &&
									e.hasOwnProperty("PartNum") &&
									(n.PartNum = e.PartNum),
								null != e.TotalPart &&
									e.hasOwnProperty("TotalPart") &&
									(n.TotalPart = e.TotalPart),
								null != e.TimeSpent &&
									e.hasOwnProperty("TimeSpent") &&
									(n.TimeSpent = e.TimeSpent),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsPlayerInfo = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.PlayingState = 0),
						(e.prototype.WatchingTime = 0),
						(e.prototype.BufferLength = 0),
						(e.prototype.Rebuffers = 0),
						(e.prototype.RebufferingTime = 0),
						(e.prototype.BandwidthFluctuation = 0),
						(e.prototype.Bandwidth = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.PlayingState &&
									e.hasOwnProperty("PlayingState") &&
									t.uint32(8).int32(e.PlayingState),
								null != e.WatchingTime &&
									e.hasOwnProperty("WatchingTime") &&
									t.uint32(21).float(e.WatchingTime),
								null != e.BufferLength &&
									e.hasOwnProperty("BufferLength") &&
									t.uint32(29).float(e.BufferLength),
								null != e.Rebuffers &&
									e.hasOwnProperty("Rebuffers") &&
									t.uint32(32).uint32(e.Rebuffers),
								null != e.RebufferingTime &&
									e.hasOwnProperty("RebufferingTime") &&
									t.uint32(45).float(e.RebufferingTime),
								null != e.BandwidthFluctuation &&
									e.hasOwnProperty("BandwidthFluctuation") &&
									t.uint32(48).uint32(e.BandwidthFluctuation),
								null != e.Bandwidth &&
									e.hasOwnProperty("Bandwidth") &&
									t.uint32(56).uint32(e.Bandwidth),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsPlayerInfo();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.PlayingState = e.int32();
										break;
									case 2:
										r.WatchingTime = e.float();
										break;
									case 3:
										r.BufferLength = e.float();
										break;
									case 4:
										r.Rebuffers = e.uint32();
										break;
									case 5:
										r.RebufferingTime = e.float();
										break;
									case 6:
										r.BandwidthFluctuation = e.uint32();
										break;
									case 7:
										r.Bandwidth = e.uint32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.PlayingState && e.hasOwnProperty("PlayingState"))
								switch (e.PlayingState) {
									default:
										return "PlayingState: enum value expected";
									case 0:
									case 1:
									case 3:
									case 4:
									case 5:
								}
							return null != e.WatchingTime &&
								e.hasOwnProperty("WatchingTime") &&
								"number" != typeof e.WatchingTime
								? "WatchingTime: number expected"
								: null != e.BufferLength &&
								  e.hasOwnProperty("BufferLength") &&
								  "number" != typeof e.BufferLength
								? "BufferLength: number expected"
								: null != e.Rebuffers &&
								  e.hasOwnProperty("Rebuffers") &&
								  !c.isInteger(e.Rebuffers)
								? "Rebuffers: integer expected"
								: null != e.RebufferingTime &&
								  e.hasOwnProperty("RebufferingTime") &&
								  "number" != typeof e.RebufferingTime
								? "RebufferingTime: number expected"
								: null != e.BandwidthFluctuation &&
								  e.hasOwnProperty("BandwidthFluctuation") &&
								  !c.isInteger(e.BandwidthFluctuation)
								? "BandwidthFluctuation: integer expected"
								: null != e.Bandwidth &&
								  e.hasOwnProperty("Bandwidth") &&
								  !c.isInteger(e.Bandwidth)
								? "Bandwidth: integer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsPlayerInfo) return e;
							var t = new l.manager.ArgumentsPlayerInfo();
							switch (e.PlayingState) {
								case "IDLE":
								case 0:
									t.PlayingState = 0;
									break;
								case "PLAYING":
								case 1:
									t.PlayingState = 1;
									break;
								case "BUFFERING":
								case 3:
									t.PlayingState = 3;
									break;
								case "PAUSED":
								case 4:
									t.PlayingState = 4;
									break;
								case "STOP":
								case 5:
									t.PlayingState = 5;
							}
							return (
								null != e.WatchingTime &&
									(t.WatchingTime = Number(e.WatchingTime)),
								null != e.BufferLength &&
									(t.BufferLength = Number(e.BufferLength)),
								null != e.Rebuffers && (t.Rebuffers = e.Rebuffers >>> 0),
								null != e.RebufferingTime &&
									(t.RebufferingTime = Number(e.RebufferingTime)),
								null != e.BandwidthFluctuation &&
									(t.BandwidthFluctuation = e.BandwidthFluctuation >>> 0),
								null != e.Bandwidth && (t.Bandwidth = e.Bandwidth >>> 0),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.PlayingState = t.enums === String ? "IDLE" : 0),
									(n.WatchingTime = 0),
									(n.BufferLength = 0),
									(n.Rebuffers = 0),
									(n.RebufferingTime = 0),
									(n.BandwidthFluctuation = 0),
									(n.Bandwidth = 0)),
								null != e.PlayingState &&
									e.hasOwnProperty("PlayingState") &&
									(n.PlayingState =
										t.enums === String
											? l.manager.PlayingState[e.PlayingState]
											: e.PlayingState),
								null != e.WatchingTime &&
									e.hasOwnProperty("WatchingTime") &&
									(n.WatchingTime =
										t.json && !isFinite(e.WatchingTime)
											? String(e.WatchingTime)
											: e.WatchingTime),
								null != e.BufferLength &&
									e.hasOwnProperty("BufferLength") &&
									(n.BufferLength =
										t.json && !isFinite(e.BufferLength)
											? String(e.BufferLength)
											: e.BufferLength),
								null != e.Rebuffers &&
									e.hasOwnProperty("Rebuffers") &&
									(n.Rebuffers = e.Rebuffers),
								null != e.RebufferingTime &&
									e.hasOwnProperty("RebufferingTime") &&
									(n.RebufferingTime =
										t.json && !isFinite(e.RebufferingTime)
											? String(e.RebufferingTime)
											: e.RebufferingTime),
								null != e.BandwidthFluctuation &&
									e.hasOwnProperty("BandwidthFluctuation") &&
									(n.BandwidthFluctuation = e.BandwidthFluctuation),
								null != e.Bandwidth &&
									e.hasOwnProperty("Bandwidth") &&
									(n.Bandwidth = e.Bandwidth),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsDeviceState = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.BatteryLevel = 0),
						(e.prototype.TotalMemory = c.Long ? c.Long.fromBits(0, 0, !0) : 0),
						(e.prototype.UsedMemory = c.Long ? c.Long.fromBits(0, 0, !0) : 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.BatteryLevel &&
									e.hasOwnProperty("BatteryLevel") &&
									t.uint32(13).float(e.BatteryLevel),
								null != e.TotalMemory &&
									e.hasOwnProperty("TotalMemory") &&
									t.uint32(16).uint64(e.TotalMemory),
								null != e.UsedMemory &&
									e.hasOwnProperty("UsedMemory") &&
									t.uint32(24).uint64(e.UsedMemory),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsDeviceState();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.BatteryLevel = e.float();
										break;
									case 2:
										r.TotalMemory = e.uint64();
										break;
									case 3:
										r.UsedMemory = e.uint64();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.BatteryLevel &&
								  e.hasOwnProperty("BatteryLevel") &&
								  "number" != typeof e.BatteryLevel
								? "BatteryLevel: number expected"
								: null != e.TotalMemory &&
								  e.hasOwnProperty("TotalMemory") &&
								  !(
										c.isInteger(e.TotalMemory) ||
										(e.TotalMemory &&
											c.isInteger(e.TotalMemory.low) &&
											c.isInteger(e.TotalMemory.high))
								  )
								? "TotalMemory: integer|Long expected"
								: null != e.UsedMemory &&
								  e.hasOwnProperty("UsedMemory") &&
								  !(
										c.isInteger(e.UsedMemory) ||
										(e.UsedMemory &&
											c.isInteger(e.UsedMemory.low) &&
											c.isInteger(e.UsedMemory.high))
								  )
								? "UsedMemory: integer|Long expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsDeviceState) return e;
							var t = new l.manager.ArgumentsDeviceState();
							return (
								null != e.BatteryLevel &&
									(t.BatteryLevel = Number(e.BatteryLevel)),
								null != e.TotalMemory &&
									(c.Long
										? ((t.TotalMemory = c.Long.fromValue(
												e.TotalMemory
										  )).unsigned = !0)
										: "string" == typeof e.TotalMemory
										? (t.TotalMemory = parseInt(e.TotalMemory, 10))
										: "number" == typeof e.TotalMemory
										? (t.TotalMemory = e.TotalMemory)
										: "object" == typeof e.TotalMemory &&
										  (t.TotalMemory = new c.LongBits(
												e.TotalMemory.low >>> 0,
												e.TotalMemory.high >>> 0
										  ).toNumber(!0))),
								null != e.UsedMemory &&
									(c.Long
										? ((t.UsedMemory = c.Long.fromValue(
												e.UsedMemory
										  )).unsigned = !0)
										: "string" == typeof e.UsedMemory
										? (t.UsedMemory = parseInt(e.UsedMemory, 10))
										: "number" == typeof e.UsedMemory
										? (t.UsedMemory = e.UsedMemory)
										: "object" == typeof e.UsedMemory &&
										  (t.UsedMemory = new c.LongBits(
												e.UsedMemory.low >>> 0,
												e.UsedMemory.high >>> 0
										  ).toNumber(!0))),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (((n.BatteryLevel = 0), c.Long)) {
									var r = new c.Long(0, 0, !0);
									n.TotalMemory =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.TotalMemory = t.longs === String ? "0" : 0;
								c.Long
									? ((r = new c.Long(0, 0, !0)),
									  (n.UsedMemory =
											t.longs === String
												? r.toString()
												: t.longs === Number
												? r.toNumber()
												: r))
									: (n.UsedMemory = t.longs === String ? "0" : 0);
							}
							return (
								null != e.BatteryLevel &&
									e.hasOwnProperty("BatteryLevel") &&
									(n.BatteryLevel =
										t.json && !isFinite(e.BatteryLevel)
											? String(e.BatteryLevel)
											: e.BatteryLevel),
								null != e.TotalMemory &&
									e.hasOwnProperty("TotalMemory") &&
									("number" == typeof e.TotalMemory
										? (n.TotalMemory =
												t.longs === String
													? String(e.TotalMemory)
													: e.TotalMemory)
										: (n.TotalMemory =
												t.longs === String
													? c.Long.prototype.toString.call(e.TotalMemory)
													: t.longs === Number
													? new c.LongBits(
															e.TotalMemory.low >>> 0,
															e.TotalMemory.high >>> 0
													  ).toNumber(!0)
													: e.TotalMemory)),
								null != e.UsedMemory &&
									e.hasOwnProperty("UsedMemory") &&
									("number" == typeof e.UsedMemory
										? (n.UsedMemory =
												t.longs === String
													? String(e.UsedMemory)
													: e.UsedMemory)
										: (n.UsedMemory =
												t.longs === String
													? c.Long.prototype.toString.call(e.UsedMemory)
													: t.longs === Number
													? new c.LongBits(
															e.UsedMemory.low >>> 0,
															e.UsedMemory.high >>> 0
													  ).toNumber(!0)
													: e.UsedMemory)),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsResourceExchanges = (function () {
					function e(e) {
						if (((this.Lists = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Lists = c.emptyArray),
						(e.prototype.Codec = ""),
						(e.prototype.Bandwidth = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if ((t || (t = u.create()), null != e.Lists && e.Lists.length))
								for (var n = 0; n < e.Lists.length; ++n)
									l.manager.ResourceExchanges.encode(
										e.Lists[n],
										t.uint32(10).fork()
									).ldelim();
							return (
								null != e.Codec &&
									e.hasOwnProperty("Codec") &&
									t.uint32(18).string(e.Codec),
								null != e.Bandwidth &&
									e.hasOwnProperty("Bandwidth") &&
									t.uint32(24).uint32(e.Bandwidth),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsResourceExchanges();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										(r.Lists && r.Lists.length) || (r.Lists = []),
											r.Lists.push(
												l.manager.ResourceExchanges.decode(e, e.uint32())
											);
										break;
									case 2:
										r.Codec = e.string();
										break;
									case 3:
										r.Bandwidth = e.uint32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.Lists && e.hasOwnProperty("Lists")) {
								if (!Array.isArray(e.Lists)) return "Lists: array expected";
								for (var t = 0; t < e.Lists.length; ++t) {
									var n = l.manager.ResourceExchanges.verify(e.Lists[t]);
									if (n) return "Lists." + n;
								}
							}
							return null != e.Codec &&
								e.hasOwnProperty("Codec") &&
								!c.isString(e.Codec)
								? "Codec: string expected"
								: null != e.Bandwidth &&
								  e.hasOwnProperty("Bandwidth") &&
								  !c.isInteger(e.Bandwidth)
								? "Bandwidth: integer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsResourceExchanges) return e;
							var t = new l.manager.ArgumentsResourceExchanges();
							if (e.Lists) {
								if (!Array.isArray(e.Lists))
									throw TypeError(
										".manager.ArgumentsResourceExchanges.Lists: array expected"
									);
								t.Lists = [];
								for (var n = 0; n < e.Lists.length; ++n) {
									if ("object" != typeof e.Lists[n])
										throw TypeError(
											".manager.ArgumentsResourceExchanges.Lists: object expected"
										);
									t.Lists[n] = l.manager.ResourceExchanges.fromObject(
										e.Lists[n]
									);
								}
							}
							return (
								null != e.Codec && (t.Codec = String(e.Codec)),
								null != e.Bandwidth && (t.Bandwidth = e.Bandwidth >>> 0),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Lists = []),
								t.defaults && ((n.Codec = ""), (n.Bandwidth = 0)),
								e.Lists && e.Lists.length)
							) {
								n.Lists = [];
								for (var r = 0; r < e.Lists.length; ++r)
									n.Lists[r] = l.manager.ResourceExchanges.toObject(
										e.Lists[r],
										t
									);
							}
							return (
								null != e.Codec &&
									e.hasOwnProperty("Codec") &&
									(n.Codec = e.Codec),
								null != e.Bandwidth &&
									e.hasOwnProperty("Bandwidth") &&
									(n.Bandwidth = e.Bandwidth),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PlayingState = (function () {
					var e = {},
						t = Object.create(e);
					return (
						(t[(e[0] = "IDLE")] = 0),
						(t[(e[1] = "PLAYING")] = 1),
						(t[(e[3] = "BUFFERING")] = 3),
						(t[(e[4] = "PAUSED")] = 4),
						(t[(e[5] = "STOP")] = 5),
						t
					);
				})()),
				(o.ResourceExchanges = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Ts = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.Pid = ""),
						(e.prototype.Pid2 = ""),
						(e.prototype.URL = ""),
						(e.prototype.URLCRC16 = 0),
						(e.prototype.TimeSpentMs = 0),
						(e.prototype.SizeBytes = 0),
						(e.prototype.Mode = ""),
						(e.prototype.Upload = !1),
						(e.prototype.Storage = c.newBuffer([])),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Ts &&
									e.hasOwnProperty("Ts") &&
									t.uint32(8).int64(e.Ts),
								null != e.Pid &&
									e.hasOwnProperty("Pid") &&
									t.uint32(18).string(e.Pid),
								null != e.Pid2 &&
									e.hasOwnProperty("Pid2") &&
									t.uint32(26).string(e.Pid2),
								null != e.URL &&
									e.hasOwnProperty("URL") &&
									t.uint32(34).string(e.URL),
								null != e.TimeSpentMs &&
									e.hasOwnProperty("TimeSpentMs") &&
									t.uint32(40).uint32(e.TimeSpentMs),
								null != e.SizeBytes &&
									e.hasOwnProperty("SizeBytes") &&
									t.uint32(56).uint32(e.SizeBytes),
								null != e.Mode &&
									e.hasOwnProperty("Mode") &&
									t.uint32(74).string(e.Mode),
								null != e.Upload &&
									e.hasOwnProperty("Upload") &&
									t.uint32(80).bool(e.Upload),
								null != e.Storage &&
									e.hasOwnProperty("Storage") &&
									t.uint32(98).bytes(e.Storage),
								null != e.URLCRC16 &&
									e.hasOwnProperty("URLCRC16") &&
									t.uint32(328).int32(e.URLCRC16),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ResourceExchanges();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Ts = e.int64();
										break;
									case 2:
										r.Pid = e.string();
										break;
									case 3:
										r.Pid2 = e.string();
										break;
									case 4:
										r.URL = e.string();
										break;
									case 41:
										r.URLCRC16 = e.int32();
										break;
									case 5:
										r.TimeSpentMs = e.uint32();
										break;
									case 7:
										r.SizeBytes = e.uint32();
										break;
									case 9:
										r.Mode = e.string();
										break;
									case 10:
										r.Upload = e.bool();
										break;
									case 12:
										r.Storage = e.bytes();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Ts &&
								  e.hasOwnProperty("Ts") &&
								  !(
										c.isInteger(e.Ts) ||
										(e.Ts && c.isInteger(e.Ts.low) && c.isInteger(e.Ts.high))
								  )
								? "Ts: integer|Long expected"
								: null != e.Pid && e.hasOwnProperty("Pid") && !c.isString(e.Pid)
								? "Pid: string expected"
								: null != e.Pid2 &&
								  e.hasOwnProperty("Pid2") &&
								  !c.isString(e.Pid2)
								? "Pid2: string expected"
								: null != e.URL && e.hasOwnProperty("URL") && !c.isString(e.URL)
								? "URL: string expected"
								: null != e.URLCRC16 &&
								  e.hasOwnProperty("URLCRC16") &&
								  !c.isInteger(e.URLCRC16)
								? "URLCRC16: integer expected"
								: null != e.TimeSpentMs &&
								  e.hasOwnProperty("TimeSpentMs") &&
								  !c.isInteger(e.TimeSpentMs)
								? "TimeSpentMs: integer expected"
								: null != e.SizeBytes &&
								  e.hasOwnProperty("SizeBytes") &&
								  !c.isInteger(e.SizeBytes)
								? "SizeBytes: integer expected"
								: null != e.Mode &&
								  e.hasOwnProperty("Mode") &&
								  !c.isString(e.Mode)
								? "Mode: string expected"
								: null != e.Upload &&
								  e.hasOwnProperty("Upload") &&
								  "boolean" != typeof e.Upload
								? "Upload: boolean expected"
								: null != e.Storage &&
								  e.hasOwnProperty("Storage") &&
								  !(
										(e.Storage && "number" == typeof e.Storage.length) ||
										c.isString(e.Storage)
								  )
								? "Storage: buffer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ResourceExchanges) return e;
							var t = new l.manager.ResourceExchanges();
							return (
								null != e.Ts &&
									(c.Long
										? ((t.Ts = c.Long.fromValue(e.Ts)).unsigned = !1)
										: "string" == typeof e.Ts
										? (t.Ts = parseInt(e.Ts, 10))
										: "number" == typeof e.Ts
										? (t.Ts = e.Ts)
										: "object" == typeof e.Ts &&
										  (t.Ts = new c.LongBits(
												e.Ts.low >>> 0,
												e.Ts.high >>> 0
										  ).toNumber())),
								null != e.Pid && (t.Pid = String(e.Pid)),
								null != e.Pid2 && (t.Pid2 = String(e.Pid2)),
								null != e.URL && (t.URL = String(e.URL)),
								null != e.URLCRC16 && (t.URLCRC16 = 0 | e.URLCRC16),
								null != e.TimeSpentMs && (t.TimeSpentMs = e.TimeSpentMs >>> 0),
								null != e.SizeBytes && (t.SizeBytes = e.SizeBytes >>> 0),
								null != e.Mode && (t.Mode = String(e.Mode)),
								null != e.Upload && (t.Upload = Boolean(e.Upload)),
								null != e.Storage &&
									("string" == typeof e.Storage
										? c.base64.decode(
												e.Storage,
												(t.Storage = c.newBuffer(c.base64.length(e.Storage))),
												0
										  )
										: e.Storage.length && (t.Storage = e.Storage)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (c.Long) {
									var r = new c.Long(0, 0, !1);
									n.Ts =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Ts = t.longs === String ? "0" : 0;
								(n.Pid = ""),
									(n.Pid2 = ""),
									(n.URL = ""),
									(n.TimeSpentMs = 0),
									(n.SizeBytes = 0),
									(n.Mode = ""),
									(n.Upload = !1),
									t.bytes === String
										? (n.Storage = "")
										: ((n.Storage = []),
										  t.bytes !== Array &&
												(n.Storage = c.newBuffer(n.Storage))),
									(n.URLCRC16 = 0);
							}
							return (
								null != e.Ts &&
									e.hasOwnProperty("Ts") &&
									("number" == typeof e.Ts
										? (n.Ts = t.longs === String ? String(e.Ts) : e.Ts)
										: (n.Ts =
												t.longs === String
													? c.Long.prototype.toString.call(e.Ts)
													: t.longs === Number
													? new c.LongBits(
															e.Ts.low >>> 0,
															e.Ts.high >>> 0
													  ).toNumber()
													: e.Ts)),
								null != e.Pid && e.hasOwnProperty("Pid") && (n.Pid = e.Pid),
								null != e.Pid2 && e.hasOwnProperty("Pid2") && (n.Pid2 = e.Pid2),
								null != e.URL && e.hasOwnProperty("URL") && (n.URL = e.URL),
								null != e.TimeSpentMs &&
									e.hasOwnProperty("TimeSpentMs") &&
									(n.TimeSpentMs = e.TimeSpentMs),
								null != e.SizeBytes &&
									e.hasOwnProperty("SizeBytes") &&
									(n.SizeBytes = e.SizeBytes),
								null != e.Mode && e.hasOwnProperty("Mode") && (n.Mode = e.Mode),
								null != e.Upload &&
									e.hasOwnProperty("Upload") &&
									(n.Upload = e.Upload),
								null != e.Storage &&
									e.hasOwnProperty("Storage") &&
									(n.Storage =
										t.bytes === String
											? c.base64.encode(e.Storage, 0, e.Storage.length)
											: t.bytes === Array
											? Array.prototype.slice.call(e.Storage)
											: e.Storage),
								null != e.URLCRC16 &&
									e.hasOwnProperty("URLCRC16") &&
									(n.URLCRC16 = e.URLCRC16),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PeerVisit = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Pid = ""),
						(e.prototype.Ts = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.Os = ""),
						(e.prototype.Browser = ""),
						(e.prototype.Content = ""),
						(e.prototype.Proto = ""),
						(e.prototype.Origin = ""),
						(e.prototype.Room = ""),
						(e.prototype.IP = ""),
						(e.prototype.Geohash = ""),
						(e.prototype.ISP = ""),
						(e.prototype.Version = ""),
						(e.prototype.Timezone = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.StartupTime = 0),
						(e.prototype.VOD = !1),
						(e.prototype.Country = ""),
						(e.prototype.City = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Pid &&
									e.hasOwnProperty("Pid") &&
									t.uint32(10).string(e.Pid),
								null != e.Ts &&
									e.hasOwnProperty("Ts") &&
									t.uint32(16).int64(e.Ts),
								null != e.Os &&
									e.hasOwnProperty("Os") &&
									t.uint32(26).string(e.Os),
								null != e.Browser &&
									e.hasOwnProperty("Browser") &&
									t.uint32(34).string(e.Browser),
								null != e.Content &&
									e.hasOwnProperty("Content") &&
									t.uint32(42).string(e.Content),
								null != e.Proto &&
									e.hasOwnProperty("Proto") &&
									t.uint32(50).string(e.Proto),
								null != e.Origin &&
									e.hasOwnProperty("Origin") &&
									t.uint32(58).string(e.Origin),
								null != e.Room &&
									e.hasOwnProperty("Room") &&
									t.uint32(66).string(e.Room),
								null != e.IP &&
									e.hasOwnProperty("IP") &&
									t.uint32(74).string(e.IP),
								null != e.Geohash &&
									e.hasOwnProperty("Geohash") &&
									t.uint32(82).string(e.Geohash),
								null != e.ISP &&
									e.hasOwnProperty("ISP") &&
									t.uint32(90).string(e.ISP),
								null != e.Version &&
									e.hasOwnProperty("Version") &&
									t.uint32(98).string(e.Version),
								null != e.Timezone &&
									e.hasOwnProperty("Timezone") &&
									t.uint32(104).int64(e.Timezone),
								null != e.StartupTime &&
									e.hasOwnProperty("StartupTime") &&
									t.uint32(117).float(e.StartupTime),
								null != e.VOD &&
									e.hasOwnProperty("VOD") &&
									t.uint32(120).bool(e.VOD),
								null != e.Country &&
									e.hasOwnProperty("Country") &&
									t.uint32(130).string(e.Country),
								null != e.City &&
									e.hasOwnProperty("City") &&
									t.uint32(138).string(e.City),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PeerVisit();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Pid = e.string();
										break;
									case 2:
										r.Ts = e.int64();
										break;
									case 3:
										r.Os = e.string();
										break;
									case 4:
										r.Browser = e.string();
										break;
									case 5:
										r.Content = e.string();
										break;
									case 6:
										r.Proto = e.string();
										break;
									case 7:
										r.Origin = e.string();
										break;
									case 8:
										r.Room = e.string();
										break;
									case 9:
										r.IP = e.string();
										break;
									case 10:
										r.Geohash = e.string();
										break;
									case 11:
										r.ISP = e.string();
										break;
									case 12:
										r.Version = e.string();
										break;
									case 13:
										r.Timezone = e.int64();
										break;
									case 14:
										r.StartupTime = e.float();
										break;
									case 15:
										r.VOD = e.bool();
										break;
									case 16:
										r.Country = e.string();
										break;
									case 17:
										r.City = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Pid && e.hasOwnProperty("Pid") && !c.isString(e.Pid)
								? "Pid: string expected"
								: null != e.Ts &&
								  e.hasOwnProperty("Ts") &&
								  !(
										c.isInteger(e.Ts) ||
										(e.Ts && c.isInteger(e.Ts.low) && c.isInteger(e.Ts.high))
								  )
								? "Ts: integer|Long expected"
								: null != e.Os && e.hasOwnProperty("Os") && !c.isString(e.Os)
								? "Os: string expected"
								: null != e.Browser &&
								  e.hasOwnProperty("Browser") &&
								  !c.isString(e.Browser)
								? "Browser: string expected"
								: null != e.Content &&
								  e.hasOwnProperty("Content") &&
								  !c.isString(e.Content)
								? "Content: string expected"
								: null != e.Proto &&
								  e.hasOwnProperty("Proto") &&
								  !c.isString(e.Proto)
								? "Proto: string expected"
								: null != e.Origin &&
								  e.hasOwnProperty("Origin") &&
								  !c.isString(e.Origin)
								? "Origin: string expected"
								: null != e.Room &&
								  e.hasOwnProperty("Room") &&
								  !c.isString(e.Room)
								? "Room: string expected"
								: null != e.IP && e.hasOwnProperty("IP") && !c.isString(e.IP)
								? "IP: string expected"
								: null != e.Geohash &&
								  e.hasOwnProperty("Geohash") &&
								  !c.isString(e.Geohash)
								? "Geohash: string expected"
								: null != e.ISP && e.hasOwnProperty("ISP") && !c.isString(e.ISP)
								? "ISP: string expected"
								: null != e.Version &&
								  e.hasOwnProperty("Version") &&
								  !c.isString(e.Version)
								? "Version: string expected"
								: null != e.Timezone &&
								  e.hasOwnProperty("Timezone") &&
								  !(
										c.isInteger(e.Timezone) ||
										(e.Timezone &&
											c.isInteger(e.Timezone.low) &&
											c.isInteger(e.Timezone.high))
								  )
								? "Timezone: integer|Long expected"
								: null != e.StartupTime &&
								  e.hasOwnProperty("StartupTime") &&
								  "number" != typeof e.StartupTime
								? "StartupTime: number expected"
								: null != e.VOD &&
								  e.hasOwnProperty("VOD") &&
								  "boolean" != typeof e.VOD
								? "VOD: boolean expected"
								: null != e.Country &&
								  e.hasOwnProperty("Country") &&
								  !c.isString(e.Country)
								? "Country: string expected"
								: null != e.City &&
								  e.hasOwnProperty("City") &&
								  !c.isString(e.City)
								? "City: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PeerVisit) return e;
							var t = new l.manager.PeerVisit();
							return (
								null != e.Pid && (t.Pid = String(e.Pid)),
								null != e.Ts &&
									(c.Long
										? ((t.Ts = c.Long.fromValue(e.Ts)).unsigned = !1)
										: "string" == typeof e.Ts
										? (t.Ts = parseInt(e.Ts, 10))
										: "number" == typeof e.Ts
										? (t.Ts = e.Ts)
										: "object" == typeof e.Ts &&
										  (t.Ts = new c.LongBits(
												e.Ts.low >>> 0,
												e.Ts.high >>> 0
										  ).toNumber())),
								null != e.Os && (t.Os = String(e.Os)),
								null != e.Browser && (t.Browser = String(e.Browser)),
								null != e.Content && (t.Content = String(e.Content)),
								null != e.Proto && (t.Proto = String(e.Proto)),
								null != e.Origin && (t.Origin = String(e.Origin)),
								null != e.Room && (t.Room = String(e.Room)),
								null != e.IP && (t.IP = String(e.IP)),
								null != e.Geohash && (t.Geohash = String(e.Geohash)),
								null != e.ISP && (t.ISP = String(e.ISP)),
								null != e.Version && (t.Version = String(e.Version)),
								null != e.Timezone &&
									(c.Long
										? ((t.Timezone = c.Long.fromValue(e.Timezone)).unsigned =
												!1)
										: "string" == typeof e.Timezone
										? (t.Timezone = parseInt(e.Timezone, 10))
										: "number" == typeof e.Timezone
										? (t.Timezone = e.Timezone)
										: "object" == typeof e.Timezone &&
										  (t.Timezone = new c.LongBits(
												e.Timezone.low >>> 0,
												e.Timezone.high >>> 0
										  ).toNumber())),
								null != e.StartupTime &&
									(t.StartupTime = Number(e.StartupTime)),
								null != e.VOD && (t.VOD = Boolean(e.VOD)),
								null != e.Country && (t.Country = String(e.Country)),
								null != e.City && (t.City = String(e.City)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (((n.Pid = ""), c.Long)) {
									var r = new c.Long(0, 0, !1);
									n.Ts =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Ts = t.longs === String ? "0" : 0;
								(n.Os = ""),
									(n.Browser = ""),
									(n.Content = ""),
									(n.Proto = ""),
									(n.Origin = ""),
									(n.Room = ""),
									(n.IP = ""),
									(n.Geohash = ""),
									(n.ISP = ""),
									(n.Version = ""),
									c.Long
										? ((r = new c.Long(0, 0, !1)),
										  (n.Timezone =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.Timezone = t.longs === String ? "0" : 0),
									(n.StartupTime = 0),
									(n.VOD = !1),
									(n.Country = ""),
									(n.City = "");
							}
							return (
								null != e.Pid && e.hasOwnProperty("Pid") && (n.Pid = e.Pid),
								null != e.Ts &&
									e.hasOwnProperty("Ts") &&
									("number" == typeof e.Ts
										? (n.Ts = t.longs === String ? String(e.Ts) : e.Ts)
										: (n.Ts =
												t.longs === String
													? c.Long.prototype.toString.call(e.Ts)
													: t.longs === Number
													? new c.LongBits(
															e.Ts.low >>> 0,
															e.Ts.high >>> 0
													  ).toNumber()
													: e.Ts)),
								null != e.Os && e.hasOwnProperty("Os") && (n.Os = e.Os),
								null != e.Browser &&
									e.hasOwnProperty("Browser") &&
									(n.Browser = e.Browser),
								null != e.Content &&
									e.hasOwnProperty("Content") &&
									(n.Content = e.Content),
								null != e.Proto &&
									e.hasOwnProperty("Proto") &&
									(n.Proto = e.Proto),
								null != e.Origin &&
									e.hasOwnProperty("Origin") &&
									(n.Origin = e.Origin),
								null != e.Room && e.hasOwnProperty("Room") && (n.Room = e.Room),
								null != e.IP && e.hasOwnProperty("IP") && (n.IP = e.IP),
								null != e.Geohash &&
									e.hasOwnProperty("Geohash") &&
									(n.Geohash = e.Geohash),
								null != e.ISP && e.hasOwnProperty("ISP") && (n.ISP = e.ISP),
								null != e.Version &&
									e.hasOwnProperty("Version") &&
									(n.Version = e.Version),
								null != e.Timezone &&
									e.hasOwnProperty("Timezone") &&
									("number" == typeof e.Timezone
										? (n.Timezone =
												t.longs === String ? String(e.Timezone) : e.Timezone)
										: (n.Timezone =
												t.longs === String
													? c.Long.prototype.toString.call(e.Timezone)
													: t.longs === Number
													? new c.LongBits(
															e.Timezone.low >>> 0,
															e.Timezone.high >>> 0
													  ).toNumber()
													: e.Timezone)),
								null != e.StartupTime &&
									e.hasOwnProperty("StartupTime") &&
									(n.StartupTime =
										t.json && !isFinite(e.StartupTime)
											? String(e.StartupTime)
											: e.StartupTime),
								null != e.VOD && e.hasOwnProperty("VOD") && (n.VOD = e.VOD),
								null != e.Country &&
									e.hasOwnProperty("Country") &&
									(n.Country = e.Country),
								null != e.City && e.hasOwnProperty("City") && (n.City = e.City),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PeeringStats = (function () {
					function e(e) {
						if (((this.MsgCounts = []), (this.MsgTimeSpent = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.TimeConnection = 0),
						(e.prototype.MsgCounts = c.emptyArray),
						(e.prototype.MsgTimeSpent = c.emptyArray),
						(e.prototype.ReasonLeave = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if (
								(t || (t = u.create()),
								null != e.TimeConnection &&
									e.hasOwnProperty("TimeConnection") &&
									t.uint32(16).uint32(e.TimeConnection),
								null != e.MsgCounts && e.MsgCounts.length)
							) {
								t.uint32(26).fork();
								for (var n = 0; n < e.MsgCounts.length; ++n)
									t.uint32(e.MsgCounts[n]);
								t.ldelim();
							}
							if (null != e.MsgTimeSpent && e.MsgTimeSpent.length) {
								for (t.uint32(34).fork(), n = 0; n < e.MsgTimeSpent.length; ++n)
									t.uint32(e.MsgTimeSpent[n]);
								t.ldelim();
							}
							return (
								null != e.ReasonLeave &&
									e.hasOwnProperty("ReasonLeave") &&
									t.uint32(42).string(e.ReasonLeave),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PeeringStats();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 2:
										r.TimeConnection = e.uint32();
										break;
									case 3:
										if (
											((r.MsgCounts && r.MsgCounts.length) ||
												(r.MsgCounts = []),
											2 == (7 & i))
										)
											for (var o = e.uint32() + e.pos; e.pos < o; )
												r.MsgCounts.push(e.uint32());
										else r.MsgCounts.push(e.uint32());
										break;
									case 4:
										if (
											((r.MsgTimeSpent && r.MsgTimeSpent.length) ||
												(r.MsgTimeSpent = []),
											2 == (7 & i))
										)
											for (o = e.uint32() + e.pos; e.pos < o; )
												r.MsgTimeSpent.push(e.uint32());
										else r.MsgTimeSpent.push(e.uint32());
										break;
									case 5:
										r.ReasonLeave = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.TimeConnection &&
								e.hasOwnProperty("TimeConnection") &&
								!c.isInteger(e.TimeConnection)
							)
								return "TimeConnection: integer expected";
							if (null != e.MsgCounts && e.hasOwnProperty("MsgCounts")) {
								if (!Array.isArray(e.MsgCounts))
									return "MsgCounts: array expected";
								for (var t = 0; t < e.MsgCounts.length; ++t)
									if (!c.isInteger(e.MsgCounts[t]))
										return "MsgCounts: integer[] expected";
							}
							if (null != e.MsgTimeSpent && e.hasOwnProperty("MsgTimeSpent")) {
								if (!Array.isArray(e.MsgTimeSpent))
									return "MsgTimeSpent: array expected";
								for (t = 0; t < e.MsgTimeSpent.length; ++t)
									if (!c.isInteger(e.MsgTimeSpent[t]))
										return "MsgTimeSpent: integer[] expected";
							}
							return null != e.ReasonLeave &&
								e.hasOwnProperty("ReasonLeave") &&
								!c.isString(e.ReasonLeave)
								? "ReasonLeave: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PeeringStats) return e;
							var t = new l.manager.PeeringStats();
							if (
								(null != e.TimeConnection &&
									(t.TimeConnection = e.TimeConnection >>> 0),
								e.MsgCounts)
							) {
								if (!Array.isArray(e.MsgCounts))
									throw TypeError(
										".manager.PeeringStats.MsgCounts: array expected"
									);
								t.MsgCounts = [];
								for (var n = 0; n < e.MsgCounts.length; ++n)
									t.MsgCounts[n] = e.MsgCounts[n] >>> 0;
							}
							if (e.MsgTimeSpent) {
								if (!Array.isArray(e.MsgTimeSpent))
									throw TypeError(
										".manager.PeeringStats.MsgTimeSpent: array expected"
									);
								for (t.MsgTimeSpent = [], n = 0; n < e.MsgTimeSpent.length; ++n)
									t.MsgTimeSpent[n] = e.MsgTimeSpent[n] >>> 0;
							}
							return (
								null != e.ReasonLeave &&
									(t.ReasonLeave = String(e.ReasonLeave)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) &&
									((n.MsgCounts = []), (n.MsgTimeSpent = [])),
								t.defaults && ((n.TimeConnection = 0), (n.ReasonLeave = "")),
								null != e.TimeConnection &&
									e.hasOwnProperty("TimeConnection") &&
									(n.TimeConnection = e.TimeConnection),
								e.MsgCounts && e.MsgCounts.length)
							) {
								n.MsgCounts = [];
								for (var r = 0; r < e.MsgCounts.length; ++r)
									n.MsgCounts[r] = e.MsgCounts[r];
							}
							if (e.MsgTimeSpent && e.MsgTimeSpent.length)
								for (n.MsgTimeSpent = [], r = 0; r < e.MsgTimeSpent.length; ++r)
									n.MsgTimeSpent[r] = e.MsgTimeSpent[r];
							return (
								null != e.ReasonLeave &&
									e.hasOwnProperty("ReasonLeave") &&
									(n.ReasonLeave = e.ReasonLeave),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PeerState = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.BufferLengthBytes = 0),
						(e.prototype.SwarmSize = 0),
						(e.prototype.OccupiedSlot = 0),
						(e.prototype.FreeSlot = 0),
						(e.prototype.WatchingTimeSec = c.Long
							? c.Long.fromBits(0, 0, !0)
							: 0),
						(e.prototype.Rebuffers = c.Long ? c.Long.fromBits(0, 0, !0) : 0),
						(e.prototype.RebufferingTime = c.Long
							? c.Long.fromBits(0, 0, !0)
							: 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.BufferLengthBytes &&
									e.hasOwnProperty("BufferLengthBytes") &&
									t.uint32(13).float(e.BufferLengthBytes),
								null != e.SwarmSize &&
									e.hasOwnProperty("SwarmSize") &&
									t.uint32(21).float(e.SwarmSize),
								null != e.OccupiedSlot &&
									e.hasOwnProperty("OccupiedSlot") &&
									t.uint32(29).float(e.OccupiedSlot),
								null != e.FreeSlot &&
									e.hasOwnProperty("FreeSlot") &&
									t.uint32(37).float(e.FreeSlot),
								null != e.WatchingTimeSec &&
									e.hasOwnProperty("WatchingTimeSec") &&
									t.uint32(40).uint64(e.WatchingTimeSec),
								null != e.Rebuffers &&
									e.hasOwnProperty("Rebuffers") &&
									t.uint32(48).uint64(e.Rebuffers),
								null != e.RebufferingTime &&
									e.hasOwnProperty("RebufferingTime") &&
									t.uint32(56).uint64(e.RebufferingTime),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PeerState();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.BufferLengthBytes = e.float();
										break;
									case 2:
										r.SwarmSize = e.float();
										break;
									case 3:
										r.OccupiedSlot = e.float();
										break;
									case 4:
										r.FreeSlot = e.float();
										break;
									case 5:
										r.WatchingTimeSec = e.uint64();
										break;
									case 6:
										r.Rebuffers = e.uint64();
										break;
									case 7:
										r.RebufferingTime = e.uint64();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.BufferLengthBytes &&
								  e.hasOwnProperty("BufferLengthBytes") &&
								  "number" != typeof e.BufferLengthBytes
								? "BufferLengthBytes: number expected"
								: null != e.SwarmSize &&
								  e.hasOwnProperty("SwarmSize") &&
								  "number" != typeof e.SwarmSize
								? "SwarmSize: number expected"
								: null != e.OccupiedSlot &&
								  e.hasOwnProperty("OccupiedSlot") &&
								  "number" != typeof e.OccupiedSlot
								? "OccupiedSlot: number expected"
								: null != e.FreeSlot &&
								  e.hasOwnProperty("FreeSlot") &&
								  "number" != typeof e.FreeSlot
								? "FreeSlot: number expected"
								: null != e.WatchingTimeSec &&
								  e.hasOwnProperty("WatchingTimeSec") &&
								  !(
										c.isInteger(e.WatchingTimeSec) ||
										(e.WatchingTimeSec &&
											c.isInteger(e.WatchingTimeSec.low) &&
											c.isInteger(e.WatchingTimeSec.high))
								  )
								? "WatchingTimeSec: integer|Long expected"
								: null != e.Rebuffers &&
								  e.hasOwnProperty("Rebuffers") &&
								  !(
										c.isInteger(e.Rebuffers) ||
										(e.Rebuffers &&
											c.isInteger(e.Rebuffers.low) &&
											c.isInteger(e.Rebuffers.high))
								  )
								? "Rebuffers: integer|Long expected"
								: null != e.RebufferingTime &&
								  e.hasOwnProperty("RebufferingTime") &&
								  !(
										c.isInteger(e.RebufferingTime) ||
										(e.RebufferingTime &&
											c.isInteger(e.RebufferingTime.low) &&
											c.isInteger(e.RebufferingTime.high))
								  )
								? "RebufferingTime: integer|Long expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PeerState) return e;
							var t = new l.manager.PeerState();
							return (
								null != e.BufferLengthBytes &&
									(t.BufferLengthBytes = Number(e.BufferLengthBytes)),
								null != e.SwarmSize && (t.SwarmSize = Number(e.SwarmSize)),
								null != e.OccupiedSlot &&
									(t.OccupiedSlot = Number(e.OccupiedSlot)),
								null != e.FreeSlot && (t.FreeSlot = Number(e.FreeSlot)),
								null != e.WatchingTimeSec &&
									(c.Long
										? ((t.WatchingTimeSec = c.Long.fromValue(
												e.WatchingTimeSec
										  )).unsigned = !0)
										: "string" == typeof e.WatchingTimeSec
										? (t.WatchingTimeSec = parseInt(e.WatchingTimeSec, 10))
										: "number" == typeof e.WatchingTimeSec
										? (t.WatchingTimeSec = e.WatchingTimeSec)
										: "object" == typeof e.WatchingTimeSec &&
										  (t.WatchingTimeSec = new c.LongBits(
												e.WatchingTimeSec.low >>> 0,
												e.WatchingTimeSec.high >>> 0
										  ).toNumber(!0))),
								null != e.Rebuffers &&
									(c.Long
										? ((t.Rebuffers = c.Long.fromValue(e.Rebuffers)).unsigned =
												!0)
										: "string" == typeof e.Rebuffers
										? (t.Rebuffers = parseInt(e.Rebuffers, 10))
										: "number" == typeof e.Rebuffers
										? (t.Rebuffers = e.Rebuffers)
										: "object" == typeof e.Rebuffers &&
										  (t.Rebuffers = new c.LongBits(
												e.Rebuffers.low >>> 0,
												e.Rebuffers.high >>> 0
										  ).toNumber(!0))),
								null != e.RebufferingTime &&
									(c.Long
										? ((t.RebufferingTime = c.Long.fromValue(
												e.RebufferingTime
										  )).unsigned = !0)
										: "string" == typeof e.RebufferingTime
										? (t.RebufferingTime = parseInt(e.RebufferingTime, 10))
										: "number" == typeof e.RebufferingTime
										? (t.RebufferingTime = e.RebufferingTime)
										: "object" == typeof e.RebufferingTime &&
										  (t.RebufferingTime = new c.LongBits(
												e.RebufferingTime.low >>> 0,
												e.RebufferingTime.high >>> 0
										  ).toNumber(!0))),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (
									((n.BufferLengthBytes = 0),
									(n.SwarmSize = 0),
									(n.OccupiedSlot = 0),
									(n.FreeSlot = 0),
									c.Long)
								) {
									var r = new c.Long(0, 0, !0);
									n.WatchingTimeSec =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.WatchingTimeSec = t.longs === String ? "0" : 0;
								c.Long
									? ((r = new c.Long(0, 0, !0)),
									  (n.Rebuffers =
											t.longs === String
												? r.toString()
												: t.longs === Number
												? r.toNumber()
												: r))
									: (n.Rebuffers = t.longs === String ? "0" : 0),
									c.Long
										? ((r = new c.Long(0, 0, !0)),
										  (n.RebufferingTime =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.RebufferingTime = t.longs === String ? "0" : 0);
							}
							return (
								null != e.BufferLengthBytes &&
									e.hasOwnProperty("BufferLengthBytes") &&
									(n.BufferLengthBytes =
										t.json && !isFinite(e.BufferLengthBytes)
											? String(e.BufferLengthBytes)
											: e.BufferLengthBytes),
								null != e.SwarmSize &&
									e.hasOwnProperty("SwarmSize") &&
									(n.SwarmSize =
										t.json && !isFinite(e.SwarmSize)
											? String(e.SwarmSize)
											: e.SwarmSize),
								null != e.OccupiedSlot &&
									e.hasOwnProperty("OccupiedSlot") &&
									(n.OccupiedSlot =
										t.json && !isFinite(e.OccupiedSlot)
											? String(e.OccupiedSlot)
											: e.OccupiedSlot),
								null != e.FreeSlot &&
									e.hasOwnProperty("FreeSlot") &&
									(n.FreeSlot =
										t.json && !isFinite(e.FreeSlot)
											? String(e.FreeSlot)
											: e.FreeSlot),
								null != e.WatchingTimeSec &&
									e.hasOwnProperty("WatchingTimeSec") &&
									("number" == typeof e.WatchingTimeSec
										? (n.WatchingTimeSec =
												t.longs === String
													? String(e.WatchingTimeSec)
													: e.WatchingTimeSec)
										: (n.WatchingTimeSec =
												t.longs === String
													? c.Long.prototype.toString.call(e.WatchingTimeSec)
													: t.longs === Number
													? new c.LongBits(
															e.WatchingTimeSec.low >>> 0,
															e.WatchingTimeSec.high >>> 0
													  ).toNumber(!0)
													: e.WatchingTimeSec)),
								null != e.Rebuffers &&
									e.hasOwnProperty("Rebuffers") &&
									("number" == typeof e.Rebuffers
										? (n.Rebuffers =
												t.longs === String ? String(e.Rebuffers) : e.Rebuffers)
										: (n.Rebuffers =
												t.longs === String
													? c.Long.prototype.toString.call(e.Rebuffers)
													: t.longs === Number
													? new c.LongBits(
															e.Rebuffers.low >>> 0,
															e.Rebuffers.high >>> 0
													  ).toNumber(!0)
													: e.Rebuffers)),
								null != e.RebufferingTime &&
									e.hasOwnProperty("RebufferingTime") &&
									("number" == typeof e.RebufferingTime
										? (n.RebufferingTime =
												t.longs === String
													? String(e.RebufferingTime)
													: e.RebufferingTime)
										: (n.RebufferingTime =
												t.longs === String
													? c.Long.prototype.toString.call(e.RebufferingTime)
													: t.longs === Number
													? new c.LongBits(
															e.RebufferingTime.low >>> 0,
															e.RebufferingTime.high >>> 0
													  ).toNumber(!0)
													: e.RebufferingTime)),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PlayerState = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Timeshift = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.Quality = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.PlayingState = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Timeshift &&
									e.hasOwnProperty("Timeshift") &&
									t.uint32(8).int64(e.Timeshift),
								null != e.Quality &&
									e.hasOwnProperty("Quality") &&
									t.uint32(16).int64(e.Quality),
								null != e.PlayingState &&
									e.hasOwnProperty("PlayingState") &&
									t.uint32(24).int32(e.PlayingState),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PlayerState();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Timeshift = e.int64();
										break;
									case 2:
										r.Quality = e.int64();
										break;
									case 3:
										r.PlayingState = e.int32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.Timeshift &&
								e.hasOwnProperty("Timeshift") &&
								!(
									c.isInteger(e.Timeshift) ||
									(e.Timeshift &&
										c.isInteger(e.Timeshift.low) &&
										c.isInteger(e.Timeshift.high))
								)
							)
								return "Timeshift: integer|Long expected";
							if (
								null != e.Quality &&
								e.hasOwnProperty("Quality") &&
								!(
									c.isInteger(e.Quality) ||
									(e.Quality &&
										c.isInteger(e.Quality.low) &&
										c.isInteger(e.Quality.high))
								)
							)
								return "Quality: integer|Long expected";
							if (null != e.PlayingState && e.hasOwnProperty("PlayingState"))
								switch (e.PlayingState) {
									default:
										return "PlayingState: enum value expected";
									case 0:
									case 1:
									case 3:
									case 4:
									case 5:
								}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PlayerState) return e;
							var t = new l.manager.PlayerState();
							switch (
								(null != e.Timeshift &&
									(c.Long
										? ((t.Timeshift = c.Long.fromValue(e.Timeshift)).unsigned =
												!1)
										: "string" == typeof e.Timeshift
										? (t.Timeshift = parseInt(e.Timeshift, 10))
										: "number" == typeof e.Timeshift
										? (t.Timeshift = e.Timeshift)
										: "object" == typeof e.Timeshift &&
										  (t.Timeshift = new c.LongBits(
												e.Timeshift.low >>> 0,
												e.Timeshift.high >>> 0
										  ).toNumber())),
								null != e.Quality &&
									(c.Long
										? ((t.Quality = c.Long.fromValue(e.Quality)).unsigned = !1)
										: "string" == typeof e.Quality
										? (t.Quality = parseInt(e.Quality, 10))
										: "number" == typeof e.Quality
										? (t.Quality = e.Quality)
										: "object" == typeof e.Quality &&
										  (t.Quality = new c.LongBits(
												e.Quality.low >>> 0,
												e.Quality.high >>> 0
										  ).toNumber())),
								e.PlayingState)
							) {
								case "IDLE":
								case 0:
									t.PlayingState = 0;
									break;
								case "PLAYING":
								case 1:
									t.PlayingState = 1;
									break;
								case "BUFFERING":
								case 3:
									t.PlayingState = 3;
									break;
								case "PAUSED":
								case 4:
									t.PlayingState = 4;
									break;
								case "STOP":
								case 5:
									t.PlayingState = 5;
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (c.Long) {
									var r = new c.Long(0, 0, !1);
									n.Timeshift =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Timeshift = t.longs === String ? "0" : 0;
								c.Long
									? ((r = new c.Long(0, 0, !1)),
									  (n.Quality =
											t.longs === String
												? r.toString()
												: t.longs === Number
												? r.toNumber()
												: r))
									: (n.Quality = t.longs === String ? "0" : 0),
									(n.PlayingState = t.enums === String ? "IDLE" : 0);
							}
							return (
								null != e.Timeshift &&
									e.hasOwnProperty("Timeshift") &&
									("number" == typeof e.Timeshift
										? (n.Timeshift =
												t.longs === String ? String(e.Timeshift) : e.Timeshift)
										: (n.Timeshift =
												t.longs === String
													? c.Long.prototype.toString.call(e.Timeshift)
													: t.longs === Number
													? new c.LongBits(
															e.Timeshift.low >>> 0,
															e.Timeshift.high >>> 0
													  ).toNumber()
													: e.Timeshift)),
								null != e.Quality &&
									e.hasOwnProperty("Quality") &&
									("number" == typeof e.Quality
										? (n.Quality =
												t.longs === String ? String(e.Quality) : e.Quality)
										: (n.Quality =
												t.longs === String
													? c.Long.prototype.toString.call(e.Quality)
													: t.longs === Number
													? new c.LongBits(
															e.Quality.low >>> 0,
															e.Quality.high >>> 0
													  ).toNumber()
													: e.Quality)),
								null != e.PlayingState &&
									e.hasOwnProperty("PlayingState") &&
									(n.PlayingState =
										t.enums === String
											? l.manager.PlayingState[e.PlayingState]
											: e.PlayingState),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PingPongExchange = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Seq = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.Pid = ""),
						(e.prototype.Start = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.End = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.State = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Seq &&
									e.hasOwnProperty("Seq") &&
									t.uint32(8).int64(e.Seq),
								null != e.Pid &&
									e.hasOwnProperty("Pid") &&
									t.uint32(18).string(e.Pid),
								null != e.Start &&
									e.hasOwnProperty("Start") &&
									t.uint32(24).int64(e.Start),
								null != e.End &&
									e.hasOwnProperty("End") &&
									t.uint32(32).int64(e.End),
								null != e.State &&
									e.hasOwnProperty("State") &&
									t.uint32(42).string(e.State),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PingPongExchange();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Seq = e.int64();
										break;
									case 2:
										r.Pid = e.string();
										break;
									case 3:
										r.Start = e.int64();
										break;
									case 4:
										r.End = e.int64();
										break;
									case 5:
										r.State = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Seq &&
								  e.hasOwnProperty("Seq") &&
								  !(
										c.isInteger(e.Seq) ||
										(e.Seq && c.isInteger(e.Seq.low) && c.isInteger(e.Seq.high))
								  )
								? "Seq: integer|Long expected"
								: null != e.Pid && e.hasOwnProperty("Pid") && !c.isString(e.Pid)
								? "Pid: string expected"
								: null != e.Start &&
								  e.hasOwnProperty("Start") &&
								  !(
										c.isInteger(e.Start) ||
										(e.Start &&
											c.isInteger(e.Start.low) &&
											c.isInteger(e.Start.high))
								  )
								? "Start: integer|Long expected"
								: null != e.End &&
								  e.hasOwnProperty("End") &&
								  !(
										c.isInteger(e.End) ||
										(e.End && c.isInteger(e.End.low) && c.isInteger(e.End.high))
								  )
								? "End: integer|Long expected"
								: null != e.State &&
								  e.hasOwnProperty("State") &&
								  !c.isString(e.State)
								? "State: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PingPongExchange) return e;
							var t = new l.manager.PingPongExchange();
							return (
								null != e.Seq &&
									(c.Long
										? ((t.Seq = c.Long.fromValue(e.Seq)).unsigned = !1)
										: "string" == typeof e.Seq
										? (t.Seq = parseInt(e.Seq, 10))
										: "number" == typeof e.Seq
										? (t.Seq = e.Seq)
										: "object" == typeof e.Seq &&
										  (t.Seq = new c.LongBits(
												e.Seq.low >>> 0,
												e.Seq.high >>> 0
										  ).toNumber())),
								null != e.Pid && (t.Pid = String(e.Pid)),
								null != e.Start &&
									(c.Long
										? ((t.Start = c.Long.fromValue(e.Start)).unsigned = !1)
										: "string" == typeof e.Start
										? (t.Start = parseInt(e.Start, 10))
										: "number" == typeof e.Start
										? (t.Start = e.Start)
										: "object" == typeof e.Start &&
										  (t.Start = new c.LongBits(
												e.Start.low >>> 0,
												e.Start.high >>> 0
										  ).toNumber())),
								null != e.End &&
									(c.Long
										? ((t.End = c.Long.fromValue(e.End)).unsigned = !1)
										: "string" == typeof e.End
										? (t.End = parseInt(e.End, 10))
										: "number" == typeof e.End
										? (t.End = e.End)
										: "object" == typeof e.End &&
										  (t.End = new c.LongBits(
												e.End.low >>> 0,
												e.End.high >>> 0
										  ).toNumber())),
								null != e.State && (t.State = String(e.State)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (c.Long) {
									var r = new c.Long(0, 0, !1);
									n.Seq =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Seq = t.longs === String ? "0" : 0;
								(n.Pid = ""),
									c.Long
										? ((r = new c.Long(0, 0, !1)),
										  (n.Start =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.Start = t.longs === String ? "0" : 0),
									c.Long
										? ((r = new c.Long(0, 0, !1)),
										  (n.End =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.End = t.longs === String ? "0" : 0),
									(n.State = "");
							}
							return (
								null != e.Seq &&
									e.hasOwnProperty("Seq") &&
									("number" == typeof e.Seq
										? (n.Seq = t.longs === String ? String(e.Seq) : e.Seq)
										: (n.Seq =
												t.longs === String
													? c.Long.prototype.toString.call(e.Seq)
													: t.longs === Number
													? new c.LongBits(
															e.Seq.low >>> 0,
															e.Seq.high >>> 0
													  ).toNumber()
													: e.Seq)),
								null != e.Pid && e.hasOwnProperty("Pid") && (n.Pid = e.Pid),
								null != e.Start &&
									e.hasOwnProperty("Start") &&
									("number" == typeof e.Start
										? (n.Start = t.longs === String ? String(e.Start) : e.Start)
										: (n.Start =
												t.longs === String
													? c.Long.prototype.toString.call(e.Start)
													: t.longs === Number
													? new c.LongBits(
															e.Start.low >>> 0,
															e.Start.high >>> 0
													  ).toNumber()
													: e.Start)),
								null != e.End &&
									e.hasOwnProperty("End") &&
									("number" == typeof e.End
										? (n.End = t.longs === String ? String(e.End) : e.End)
										: (n.End =
												t.longs === String
													? c.Long.prototype.toString.call(e.End)
													: t.longs === Number
													? new c.LongBits(
															e.End.low >>> 0,
															e.End.high >>> 0
													  ).toNumber()
													: e.End)),
								null != e.State &&
									e.hasOwnProperty("State") &&
									(n.State = e.State),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PingPongDelay = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Pid = ""),
						(e.prototype.AvgDelayMs = 0),
						(e.prototype.MedianDelayMs = 0),
						(e.prototype.LastSeq = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.Count = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Pid &&
									e.hasOwnProperty("Pid") &&
									t.uint32(10).string(e.Pid),
								null != e.AvgDelayMs &&
									e.hasOwnProperty("AvgDelayMs") &&
									t.uint32(17).double(e.AvgDelayMs),
								null != e.MedianDelayMs &&
									e.hasOwnProperty("MedianDelayMs") &&
									t.uint32(25).double(e.MedianDelayMs),
								null != e.LastSeq &&
									e.hasOwnProperty("LastSeq") &&
									t.uint32(32).int64(e.LastSeq),
								null != e.Count &&
									e.hasOwnProperty("Count") &&
									t.uint32(40).int64(e.Count),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PingPongDelay();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Pid = e.string();
										break;
									case 2:
										r.AvgDelayMs = e.double();
										break;
									case 3:
										r.MedianDelayMs = e.double();
										break;
									case 4:
										r.LastSeq = e.int64();
										break;
									case 5:
										r.Count = e.int64();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Pid && e.hasOwnProperty("Pid") && !c.isString(e.Pid)
								? "Pid: string expected"
								: null != e.AvgDelayMs &&
								  e.hasOwnProperty("AvgDelayMs") &&
								  "number" != typeof e.AvgDelayMs
								? "AvgDelayMs: number expected"
								: null != e.MedianDelayMs &&
								  e.hasOwnProperty("MedianDelayMs") &&
								  "number" != typeof e.MedianDelayMs
								? "MedianDelayMs: number expected"
								: null != e.LastSeq &&
								  e.hasOwnProperty("LastSeq") &&
								  !(
										c.isInteger(e.LastSeq) ||
										(e.LastSeq &&
											c.isInteger(e.LastSeq.low) &&
											c.isInteger(e.LastSeq.high))
								  )
								? "LastSeq: integer|Long expected"
								: null != e.Count &&
								  e.hasOwnProperty("Count") &&
								  !(
										c.isInteger(e.Count) ||
										(e.Count &&
											c.isInteger(e.Count.low) &&
											c.isInteger(e.Count.high))
								  )
								? "Count: integer|Long expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PingPongDelay) return e;
							var t = new l.manager.PingPongDelay();
							return (
								null != e.Pid && (t.Pid = String(e.Pid)),
								null != e.AvgDelayMs && (t.AvgDelayMs = Number(e.AvgDelayMs)),
								null != e.MedianDelayMs &&
									(t.MedianDelayMs = Number(e.MedianDelayMs)),
								null != e.LastSeq &&
									(c.Long
										? ((t.LastSeq = c.Long.fromValue(e.LastSeq)).unsigned = !1)
										: "string" == typeof e.LastSeq
										? (t.LastSeq = parseInt(e.LastSeq, 10))
										: "number" == typeof e.LastSeq
										? (t.LastSeq = e.LastSeq)
										: "object" == typeof e.LastSeq &&
										  (t.LastSeq = new c.LongBits(
												e.LastSeq.low >>> 0,
												e.LastSeq.high >>> 0
										  ).toNumber())),
								null != e.Count &&
									(c.Long
										? ((t.Count = c.Long.fromValue(e.Count)).unsigned = !1)
										: "string" == typeof e.Count
										? (t.Count = parseInt(e.Count, 10))
										: "number" == typeof e.Count
										? (t.Count = e.Count)
										: "object" == typeof e.Count &&
										  (t.Count = new c.LongBits(
												e.Count.low >>> 0,
												e.Count.high >>> 0
										  ).toNumber())),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (
									((n.Pid = ""),
									(n.AvgDelayMs = 0),
									(n.MedianDelayMs = 0),
									c.Long)
								) {
									var r = new c.Long(0, 0, !1);
									n.LastSeq =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.LastSeq = t.longs === String ? "0" : 0;
								c.Long
									? ((r = new c.Long(0, 0, !1)),
									  (n.Count =
											t.longs === String
												? r.toString()
												: t.longs === Number
												? r.toNumber()
												: r))
									: (n.Count = t.longs === String ? "0" : 0);
							}
							return (
								null != e.Pid && e.hasOwnProperty("Pid") && (n.Pid = e.Pid),
								null != e.AvgDelayMs &&
									e.hasOwnProperty("AvgDelayMs") &&
									(n.AvgDelayMs =
										t.json && !isFinite(e.AvgDelayMs)
											? String(e.AvgDelayMs)
											: e.AvgDelayMs),
								null != e.MedianDelayMs &&
									e.hasOwnProperty("MedianDelayMs") &&
									(n.MedianDelayMs =
										t.json && !isFinite(e.MedianDelayMs)
											? String(e.MedianDelayMs)
											: e.MedianDelayMs),
								null != e.LastSeq &&
									e.hasOwnProperty("LastSeq") &&
									("number" == typeof e.LastSeq
										? (n.LastSeq =
												t.longs === String ? String(e.LastSeq) : e.LastSeq)
										: (n.LastSeq =
												t.longs === String
													? c.Long.prototype.toString.call(e.LastSeq)
													: t.longs === Number
													? new c.LongBits(
															e.LastSeq.low >>> 0,
															e.LastSeq.high >>> 0
													  ).toNumber()
													: e.LastSeq)),
								null != e.Count &&
									e.hasOwnProperty("Count") &&
									("number" == typeof e.Count
										? (n.Count = t.longs === String ? String(e.Count) : e.Count)
										: (n.Count =
												t.longs === String
													? c.Long.prototype.toString.call(e.Count)
													: t.longs === Number
													? new c.LongBits(
															e.Count.low >>> 0,
															e.Count.high >>> 0
													  ).toNumber()
													: e.Count)),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.NetworkInfo = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.NetworkType = ""),
						(e.prototype.Downlink = 0),
						(e.prototype.RTT = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.NetworkType &&
									e.hasOwnProperty("NetworkType") &&
									t.uint32(10).string(e.NetworkType),
								null != e.Downlink &&
									e.hasOwnProperty("Downlink") &&
									t.uint32(21).float(e.Downlink),
								null != e.RTT &&
									e.hasOwnProperty("RTT") &&
									t.uint32(29).float(e.RTT),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.NetworkInfo();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.NetworkType = e.string();
										break;
									case 2:
										r.Downlink = e.float();
										break;
									case 3:
										r.RTT = e.float();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.NetworkType &&
								  e.hasOwnProperty("NetworkType") &&
								  !c.isString(e.NetworkType)
								? "NetworkType: string expected"
								: null != e.Downlink &&
								  e.hasOwnProperty("Downlink") &&
								  "number" != typeof e.Downlink
								? "Downlink: number expected"
								: null != e.RTT &&
								  e.hasOwnProperty("RTT") &&
								  "number" != typeof e.RTT
								? "RTT: number expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.NetworkInfo) return e;
							var t = new l.manager.NetworkInfo();
							return (
								null != e.NetworkType &&
									(t.NetworkType = String(e.NetworkType)),
								null != e.Downlink && (t.Downlink = Number(e.Downlink)),
								null != e.RTT && (t.RTT = Number(e.RTT)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.NetworkType = ""), (n.Downlink = 0), (n.RTT = 0)),
								null != e.NetworkType &&
									e.hasOwnProperty("NetworkType") &&
									(n.NetworkType = e.NetworkType),
								null != e.Downlink &&
									e.hasOwnProperty("Downlink") &&
									(n.Downlink =
										t.json && !isFinite(e.Downlink)
											? String(e.Downlink)
											: e.Downlink),
								null != e.RTT &&
									e.hasOwnProperty("RTT") &&
									(n.RTT = t.json && !isFinite(e.RTT) ? String(e.RTT) : e.RTT),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.PlayerEvent = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Type = ""),
						(e.prototype.MediaType = ""),
						(e.prototype.Error = ""),
						(e.prototype.Quality = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.URL = ""),
						(e.prototype.Supplements = ""),
						(e.prototype.BufferLength = 0),
						(e.prototype.Codec = ""),
						(e.prototype.TimeShift = c.Long ? c.Long.fromBits(0, 0, !1) : 0),
						(e.prototype.DeviceBatteryLevel = 0),
						(e.prototype.DeviceTotalMemory = c.Long
							? c.Long.fromBits(0, 0, !0)
							: 0),
						(e.prototype.DeviceUsedMemory = c.Long
							? c.Long.fromBits(0, 0, !0)
							: 0),
						(e.prototype.CurrentTime = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									t.uint32(10).string(e.Type),
								null != e.MediaType &&
									e.hasOwnProperty("MediaType") &&
									t.uint32(18).string(e.MediaType),
								null != e.Error &&
									e.hasOwnProperty("Error") &&
									t.uint32(26).string(e.Error),
								null != e.Quality &&
									e.hasOwnProperty("Quality") &&
									t.uint32(32).int64(e.Quality),
								null != e.URL &&
									e.hasOwnProperty("URL") &&
									t.uint32(42).string(e.URL),
								null != e.Supplements &&
									e.hasOwnProperty("Supplements") &&
									t.uint32(50).string(e.Supplements),
								null != e.BufferLength &&
									e.hasOwnProperty("BufferLength") &&
									t.uint32(61).float(e.BufferLength),
								null != e.Codec &&
									e.hasOwnProperty("Codec") &&
									t.uint32(66).string(e.Codec),
								null != e.TimeShift &&
									e.hasOwnProperty("TimeShift") &&
									t.uint32(72).int64(e.TimeShift),
								null != e.DeviceBatteryLevel &&
									e.hasOwnProperty("DeviceBatteryLevel") &&
									t.uint32(85).float(e.DeviceBatteryLevel),
								null != e.DeviceTotalMemory &&
									e.hasOwnProperty("DeviceTotalMemory") &&
									t.uint32(88).uint64(e.DeviceTotalMemory),
								null != e.DeviceUsedMemory &&
									e.hasOwnProperty("DeviceUsedMemory") &&
									t.uint32(96).uint64(e.DeviceUsedMemory),
								null != e.CurrentTime &&
									e.hasOwnProperty("CurrentTime") &&
									t.uint32(109).float(e.CurrentTime),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.PlayerEvent();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Type = e.string();
										break;
									case 2:
										r.MediaType = e.string();
										break;
									case 3:
										r.Error = e.string();
										break;
									case 4:
										r.Quality = e.int64();
										break;
									case 5:
										r.URL = e.string();
										break;
									case 6:
										r.Supplements = e.string();
										break;
									case 7:
										r.BufferLength = e.float();
										break;
									case 8:
										r.Codec = e.string();
										break;
									case 9:
										r.TimeShift = e.int64();
										break;
									case 10:
										r.DeviceBatteryLevel = e.float();
										break;
									case 11:
										r.DeviceTotalMemory = e.uint64();
										break;
									case 12:
										r.DeviceUsedMemory = e.uint64();
										break;
									case 13:
										r.CurrentTime = e.float();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Type &&
								  e.hasOwnProperty("Type") &&
								  !c.isString(e.Type)
								? "Type: string expected"
								: null != e.MediaType &&
								  e.hasOwnProperty("MediaType") &&
								  !c.isString(e.MediaType)
								? "MediaType: string expected"
								: null != e.Error &&
								  e.hasOwnProperty("Error") &&
								  !c.isString(e.Error)
								? "Error: string expected"
								: null != e.Quality &&
								  e.hasOwnProperty("Quality") &&
								  !(
										c.isInteger(e.Quality) ||
										(e.Quality &&
											c.isInteger(e.Quality.low) &&
											c.isInteger(e.Quality.high))
								  )
								? "Quality: integer|Long expected"
								: null != e.URL && e.hasOwnProperty("URL") && !c.isString(e.URL)
								? "URL: string expected"
								: null != e.Supplements &&
								  e.hasOwnProperty("Supplements") &&
								  !c.isString(e.Supplements)
								? "Supplements: string expected"
								: null != e.BufferLength &&
								  e.hasOwnProperty("BufferLength") &&
								  "number" != typeof e.BufferLength
								? "BufferLength: number expected"
								: null != e.Codec &&
								  e.hasOwnProperty("Codec") &&
								  !c.isString(e.Codec)
								? "Codec: string expected"
								: null != e.TimeShift &&
								  e.hasOwnProperty("TimeShift") &&
								  !(
										c.isInteger(e.TimeShift) ||
										(e.TimeShift &&
											c.isInteger(e.TimeShift.low) &&
											c.isInteger(e.TimeShift.high))
								  )
								? "TimeShift: integer|Long expected"
								: null != e.DeviceBatteryLevel &&
								  e.hasOwnProperty("DeviceBatteryLevel") &&
								  "number" != typeof e.DeviceBatteryLevel
								? "DeviceBatteryLevel: number expected"
								: null != e.DeviceTotalMemory &&
								  e.hasOwnProperty("DeviceTotalMemory") &&
								  !(
										c.isInteger(e.DeviceTotalMemory) ||
										(e.DeviceTotalMemory &&
											c.isInteger(e.DeviceTotalMemory.low) &&
											c.isInteger(e.DeviceTotalMemory.high))
								  )
								? "DeviceTotalMemory: integer|Long expected"
								: null != e.DeviceUsedMemory &&
								  e.hasOwnProperty("DeviceUsedMemory") &&
								  !(
										c.isInteger(e.DeviceUsedMemory) ||
										(e.DeviceUsedMemory &&
											c.isInteger(e.DeviceUsedMemory.low) &&
											c.isInteger(e.DeviceUsedMemory.high))
								  )
								? "DeviceUsedMemory: integer|Long expected"
								: null != e.CurrentTime &&
								  e.hasOwnProperty("CurrentTime") &&
								  "number" != typeof e.CurrentTime
								? "CurrentTime: number expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.PlayerEvent) return e;
							var t = new l.manager.PlayerEvent();
							return (
								null != e.Type && (t.Type = String(e.Type)),
								null != e.MediaType && (t.MediaType = String(e.MediaType)),
								null != e.Error && (t.Error = String(e.Error)),
								null != e.Quality &&
									(c.Long
										? ((t.Quality = c.Long.fromValue(e.Quality)).unsigned = !1)
										: "string" == typeof e.Quality
										? (t.Quality = parseInt(e.Quality, 10))
										: "number" == typeof e.Quality
										? (t.Quality = e.Quality)
										: "object" == typeof e.Quality &&
										  (t.Quality = new c.LongBits(
												e.Quality.low >>> 0,
												e.Quality.high >>> 0
										  ).toNumber())),
								null != e.URL && (t.URL = String(e.URL)),
								null != e.Supplements &&
									(t.Supplements = String(e.Supplements)),
								null != e.BufferLength &&
									(t.BufferLength = Number(e.BufferLength)),
								null != e.Codec && (t.Codec = String(e.Codec)),
								null != e.TimeShift &&
									(c.Long
										? ((t.TimeShift = c.Long.fromValue(e.TimeShift)).unsigned =
												!1)
										: "string" == typeof e.TimeShift
										? (t.TimeShift = parseInt(e.TimeShift, 10))
										: "number" == typeof e.TimeShift
										? (t.TimeShift = e.TimeShift)
										: "object" == typeof e.TimeShift &&
										  (t.TimeShift = new c.LongBits(
												e.TimeShift.low >>> 0,
												e.TimeShift.high >>> 0
										  ).toNumber())),
								null != e.DeviceBatteryLevel &&
									(t.DeviceBatteryLevel = Number(e.DeviceBatteryLevel)),
								null != e.DeviceTotalMemory &&
									(c.Long
										? ((t.DeviceTotalMemory = c.Long.fromValue(
												e.DeviceTotalMemory
										  )).unsigned = !0)
										: "string" == typeof e.DeviceTotalMemory
										? (t.DeviceTotalMemory = parseInt(e.DeviceTotalMemory, 10))
										: "number" == typeof e.DeviceTotalMemory
										? (t.DeviceTotalMemory = e.DeviceTotalMemory)
										: "object" == typeof e.DeviceTotalMemory &&
										  (t.DeviceTotalMemory = new c.LongBits(
												e.DeviceTotalMemory.low >>> 0,
												e.DeviceTotalMemory.high >>> 0
										  ).toNumber(!0))),
								null != e.DeviceUsedMemory &&
									(c.Long
										? ((t.DeviceUsedMemory = c.Long.fromValue(
												e.DeviceUsedMemory
										  )).unsigned = !0)
										: "string" == typeof e.DeviceUsedMemory
										? (t.DeviceUsedMemory = parseInt(e.DeviceUsedMemory, 10))
										: "number" == typeof e.DeviceUsedMemory
										? (t.DeviceUsedMemory = e.DeviceUsedMemory)
										: "object" == typeof e.DeviceUsedMemory &&
										  (t.DeviceUsedMemory = new c.LongBits(
												e.DeviceUsedMemory.low >>> 0,
												e.DeviceUsedMemory.high >>> 0
										  ).toNumber(!0))),
								null != e.CurrentTime &&
									(t.CurrentTime = Number(e.CurrentTime)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (t.defaults) {
								if (
									((n.Type = ""), (n.MediaType = ""), (n.Error = ""), c.Long)
								) {
									var r = new c.Long(0, 0, !1);
									n.Quality =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Quality = t.longs === String ? "0" : 0;
								(n.URL = ""),
									(n.Supplements = ""),
									(n.BufferLength = 0),
									(n.Codec = ""),
									c.Long
										? ((r = new c.Long(0, 0, !1)),
										  (n.TimeShift =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.TimeShift = t.longs === String ? "0" : 0),
									(n.DeviceBatteryLevel = 0),
									c.Long
										? ((r = new c.Long(0, 0, !0)),
										  (n.DeviceTotalMemory =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.DeviceTotalMemory = t.longs === String ? "0" : 0),
									c.Long
										? ((r = new c.Long(0, 0, !0)),
										  (n.DeviceUsedMemory =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.DeviceUsedMemory = t.longs === String ? "0" : 0),
									(n.CurrentTime = 0);
							}
							return (
								null != e.Type && e.hasOwnProperty("Type") && (n.Type = e.Type),
								null != e.MediaType &&
									e.hasOwnProperty("MediaType") &&
									(n.MediaType = e.MediaType),
								null != e.Error &&
									e.hasOwnProperty("Error") &&
									(n.Error = e.Error),
								null != e.Quality &&
									e.hasOwnProperty("Quality") &&
									("number" == typeof e.Quality
										? (n.Quality =
												t.longs === String ? String(e.Quality) : e.Quality)
										: (n.Quality =
												t.longs === String
													? c.Long.prototype.toString.call(e.Quality)
													: t.longs === Number
													? new c.LongBits(
															e.Quality.low >>> 0,
															e.Quality.high >>> 0
													  ).toNumber()
													: e.Quality)),
								null != e.URL && e.hasOwnProperty("URL") && (n.URL = e.URL),
								null != e.Supplements &&
									e.hasOwnProperty("Supplements") &&
									(n.Supplements = e.Supplements),
								null != e.BufferLength &&
									e.hasOwnProperty("BufferLength") &&
									(n.BufferLength =
										t.json && !isFinite(e.BufferLength)
											? String(e.BufferLength)
											: e.BufferLength),
								null != e.Codec &&
									e.hasOwnProperty("Codec") &&
									(n.Codec = e.Codec),
								null != e.TimeShift &&
									e.hasOwnProperty("TimeShift") &&
									("number" == typeof e.TimeShift
										? (n.TimeShift =
												t.longs === String ? String(e.TimeShift) : e.TimeShift)
										: (n.TimeShift =
												t.longs === String
													? c.Long.prototype.toString.call(e.TimeShift)
													: t.longs === Number
													? new c.LongBits(
															e.TimeShift.low >>> 0,
															e.TimeShift.high >>> 0
													  ).toNumber()
													: e.TimeShift)),
								null != e.DeviceBatteryLevel &&
									e.hasOwnProperty("DeviceBatteryLevel") &&
									(n.DeviceBatteryLevel =
										t.json && !isFinite(e.DeviceBatteryLevel)
											? String(e.DeviceBatteryLevel)
											: e.DeviceBatteryLevel),
								null != e.DeviceTotalMemory &&
									e.hasOwnProperty("DeviceTotalMemory") &&
									("number" == typeof e.DeviceTotalMemory
										? (n.DeviceTotalMemory =
												t.longs === String
													? String(e.DeviceTotalMemory)
													: e.DeviceTotalMemory)
										: (n.DeviceTotalMemory =
												t.longs === String
													? c.Long.prototype.toString.call(e.DeviceTotalMemory)
													: t.longs === Number
													? new c.LongBits(
															e.DeviceTotalMemory.low >>> 0,
															e.DeviceTotalMemory.high >>> 0
													  ).toNumber(!0)
													: e.DeviceTotalMemory)),
								null != e.DeviceUsedMemory &&
									e.hasOwnProperty("DeviceUsedMemory") &&
									("number" == typeof e.DeviceUsedMemory
										? (n.DeviceUsedMemory =
												t.longs === String
													? String(e.DeviceUsedMemory)
													: e.DeviceUsedMemory)
										: (n.DeviceUsedMemory =
												t.longs === String
													? c.Long.prototype.toString.call(e.DeviceUsedMemory)
													: t.longs === Number
													? new c.LongBits(
															e.DeviceUsedMemory.low >>> 0,
															e.DeviceUsedMemory.high >>> 0
													  ).toNumber(!0)
													: e.DeviceUsedMemory)),
								null != e.CurrentTime &&
									e.hasOwnProperty("CurrentTime") &&
									(n.CurrentTime =
										t.json && !isFinite(e.CurrentTime)
											? String(e.CurrentTime)
											: e.CurrentTime),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ResourceAvailability = (function () {
					function e(e) {
						if (((this.Pids = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.URL = ""),
						(e.prototype.Pids = c.emptyArray),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if (
								(t || (t = u.create()),
								null != e.URL &&
									e.hasOwnProperty("URL") &&
									t.uint32(10).string(e.URL),
								null != e.Pids && e.Pids.length)
							)
								for (var n = 0; n < e.Pids.length; ++n)
									t.uint32(18).string(e.Pids[n]);
							return t;
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ResourceAvailability();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.URL = e.string();
										break;
									case 2:
										(r.Pids && r.Pids.length) || (r.Pids = []),
											r.Pids.push(e.string());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.URL &&
								e.hasOwnProperty("URL") &&
								!c.isString(e.URL)
							)
								return "URL: string expected";
							if (null != e.Pids && e.hasOwnProperty("Pids")) {
								if (!Array.isArray(e.Pids)) return "Pids: array expected";
								for (var t = 0; t < e.Pids.length; ++t)
									if (!c.isString(e.Pids[t])) return "Pids: string[] expected";
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ResourceAvailability) return e;
							var t = new l.manager.ResourceAvailability();
							if ((null != e.URL && (t.URL = String(e.URL)), e.Pids)) {
								if (!Array.isArray(e.Pids))
									throw TypeError(
										".manager.ResourceAvailability.Pids: array expected"
									);
								t.Pids = [];
								for (var n = 0; n < e.Pids.length; ++n)
									t.Pids[n] = String(e.Pids[n]);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Pids = []),
								t.defaults && (n.URL = ""),
								null != e.URL && e.hasOwnProperty("URL") && (n.URL = e.URL),
								e.Pids && e.Pids.length)
							) {
								n.Pids = [];
								for (var r = 0; r < e.Pids.length; ++r) n.Pids[r] = e.Pids[r];
							}
							return n;
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsRegister = (function () {
					function e(e) {
						if (((this.Candidates = []), e))
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Url = ""),
						(e.prototype.Candidates = c.emptyArray),
						(e.prototype.Bandwidth = c.Long ? c.Long.fromBits(0, 0, !0) : 0),
						(e.prototype.Codec = ""),
						(e.prototype.TimeShift = c.Long ? c.Long.fromBits(0, 0, !0) : 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							if (
								(t || (t = u.create()),
								null != e.Url &&
									e.hasOwnProperty("Url") &&
									t.uint32(18).string(e.Url),
								null != e.Candidates && e.Candidates.length)
							)
								for (var n = 0; n < e.Candidates.length; ++n)
									l.manager.IceCandidate.encode(
										e.Candidates[n],
										t.uint32(26).fork()
									).ldelim();
							return (
								null != e.Bandwidth &&
									e.hasOwnProperty("Bandwidth") &&
									t.uint32(32).uint64(e.Bandwidth),
								null != e.Codec &&
									e.hasOwnProperty("Codec") &&
									t.uint32(42).string(e.Codec),
								null != e.TimeShift &&
									e.hasOwnProperty("TimeShift") &&
									t.uint32(48).uint64(e.TimeShift),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsRegister();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 2:
										r.Url = e.string();
										break;
									case 3:
										(r.Candidates && r.Candidates.length) ||
											(r.Candidates = []),
											r.Candidates.push(
												l.manager.IceCandidate.decode(e, e.uint32())
											);
										break;
									case 4:
										r.Bandwidth = e.uint64();
										break;
									case 5:
										r.Codec = e.string();
										break;
									case 6:
										r.TimeShift = e.uint64();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (
								null != e.Url &&
								e.hasOwnProperty("Url") &&
								!c.isString(e.Url)
							)
								return "Url: string expected";
							if (null != e.Candidates && e.hasOwnProperty("Candidates")) {
								if (!Array.isArray(e.Candidates))
									return "Candidates: array expected";
								for (var t = 0; t < e.Candidates.length; ++t) {
									var n = l.manager.IceCandidate.verify(e.Candidates[t]);
									if (n) return "Candidates." + n;
								}
							}
							return null != e.Bandwidth &&
								e.hasOwnProperty("Bandwidth") &&
								!(
									c.isInteger(e.Bandwidth) ||
									(e.Bandwidth &&
										c.isInteger(e.Bandwidth.low) &&
										c.isInteger(e.Bandwidth.high))
								)
								? "Bandwidth: integer|Long expected"
								: null != e.Codec &&
								  e.hasOwnProperty("Codec") &&
								  !c.isString(e.Codec)
								? "Codec: string expected"
								: null != e.TimeShift &&
								  e.hasOwnProperty("TimeShift") &&
								  !(
										c.isInteger(e.TimeShift) ||
										(e.TimeShift &&
											c.isInteger(e.TimeShift.low) &&
											c.isInteger(e.TimeShift.high))
								  )
								? "TimeShift: integer|Long expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsRegister) return e;
							var t = new l.manager.ArgumentsRegister();
							if ((null != e.Url && (t.Url = String(e.Url)), e.Candidates)) {
								if (!Array.isArray(e.Candidates))
									throw TypeError(
										".manager.ArgumentsRegister.Candidates: array expected"
									);
								t.Candidates = [];
								for (var n = 0; n < e.Candidates.length; ++n) {
									if ("object" != typeof e.Candidates[n])
										throw TypeError(
											".manager.ArgumentsRegister.Candidates: object expected"
										);
									t.Candidates[n] = l.manager.IceCandidate.fromObject(
										e.Candidates[n]
									);
								}
							}
							return (
								null != e.Bandwidth &&
									(c.Long
										? ((t.Bandwidth = c.Long.fromValue(e.Bandwidth)).unsigned =
												!0)
										: "string" == typeof e.Bandwidth
										? (t.Bandwidth = parseInt(e.Bandwidth, 10))
										: "number" == typeof e.Bandwidth
										? (t.Bandwidth = e.Bandwidth)
										: "object" == typeof e.Bandwidth &&
										  (t.Bandwidth = new c.LongBits(
												e.Bandwidth.low >>> 0,
												e.Bandwidth.high >>> 0
										  ).toNumber(!0))),
								null != e.Codec && (t.Codec = String(e.Codec)),
								null != e.TimeShift &&
									(c.Long
										? ((t.TimeShift = c.Long.fromValue(e.TimeShift)).unsigned =
												!0)
										: "string" == typeof e.TimeShift
										? (t.TimeShift = parseInt(e.TimeShift, 10))
										: "number" == typeof e.TimeShift
										? (t.TimeShift = e.TimeShift)
										: "object" == typeof e.TimeShift &&
										  (t.TimeShift = new c.LongBits(
												e.TimeShift.low >>> 0,
												e.TimeShift.high >>> 0
										  ).toNumber(!0))),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							if (
								((t.arrays || t.defaults) && (n.Candidates = []), t.defaults)
							) {
								if (((n.Url = ""), c.Long)) {
									var r = new c.Long(0, 0, !0);
									n.Bandwidth =
										t.longs === String
											? r.toString()
											: t.longs === Number
											? r.toNumber()
											: r;
								} else n.Bandwidth = t.longs === String ? "0" : 0;
								(n.Codec = ""),
									c.Long
										? ((r = new c.Long(0, 0, !0)),
										  (n.TimeShift =
												t.longs === String
													? r.toString()
													: t.longs === Number
													? r.toNumber()
													: r))
										: (n.TimeShift = t.longs === String ? "0" : 0);
							}
							if (
								(null != e.Url && e.hasOwnProperty("Url") && (n.Url = e.Url),
								e.Candidates && e.Candidates.length)
							) {
								n.Candidates = [];
								for (var i = 0; i < e.Candidates.length; ++i)
									n.Candidates[i] = l.manager.IceCandidate.toObject(
										e.Candidates[i],
										t
									);
							}
							return (
								null != e.Bandwidth &&
									e.hasOwnProperty("Bandwidth") &&
									("number" == typeof e.Bandwidth
										? (n.Bandwidth =
												t.longs === String ? String(e.Bandwidth) : e.Bandwidth)
										: (n.Bandwidth =
												t.longs === String
													? c.Long.prototype.toString.call(e.Bandwidth)
													: t.longs === Number
													? new c.LongBits(
															e.Bandwidth.low >>> 0,
															e.Bandwidth.high >>> 0
													  ).toNumber(!0)
													: e.Bandwidth)),
								null != e.Codec &&
									e.hasOwnProperty("Codec") &&
									(n.Codec = e.Codec),
								null != e.TimeShift &&
									e.hasOwnProperty("TimeShift") &&
									("number" == typeof e.TimeShift
										? (n.TimeShift =
												t.longs === String ? String(e.TimeShift) : e.TimeShift)
										: (n.TimeShift =
												t.longs === String
													? c.Long.prototype.toString.call(e.TimeShift)
													: t.longs === Number
													? new c.LongBits(
															e.TimeShift.low >>> 0,
															e.TimeShift.high >>> 0
													  ).toNumber(!0)
													: e.TimeShift)),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsRegistered = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.ID = ""),
						(e.prototype.ISP = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.ID &&
									e.hasOwnProperty("ID") &&
									t.uint32(10).string(e.ID),
								null != e.ISP &&
									e.hasOwnProperty("ISP") &&
									t.uint32(18).string(e.ISP),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsRegistered();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.ID = e.string();
										break;
									case 2:
										r.ISP = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.ID && e.hasOwnProperty("ID") && !c.isString(e.ID)
								? "ID: string expected"
								: null != e.ISP && e.hasOwnProperty("ISP") && !c.isString(e.ISP)
								? "ISP: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsRegistered) return e;
							var t = new l.manager.ArgumentsRegistered();
							return (
								null != e.ID && (t.ID = String(e.ID)),
								null != e.ISP && (t.ISP = String(e.ISP)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults && ((n.ID = ""), (n.ISP = "")),
								null != e.ID && e.hasOwnProperty("ID") && (n.ID = e.ID),
								null != e.ISP && e.hasOwnProperty("ISP") && (n.ISP = e.ISP),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.UnregisterReason = (function () {
					var e = {},
						t = Object.create(e);
					return (
						(t[(e[0] = "UnknownUnregisterReason")] = 0),
						(t[(e[1] = "UnregisterPlaybackPaused")] = 1),
						(t[(e[2] = "UnregisterFinished")] = 2),
						(t[(e[3] = "UnregisterClosed")] = 3),
						(t[(e[4] = "UnregisterSwitching")] = 4),
						t
					);
				})()),
				(o.ArgumentsUnregister = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Reason = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Reason &&
									e.hasOwnProperty("Reason") &&
									t.uint32(8).int32(e.Reason),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.manager.ArgumentsUnregister();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Reason = e.int32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							if (null != e.Reason && e.hasOwnProperty("Reason"))
								switch (e.Reason) {
									default:
										return "Reason: enum value expected";
									case 0:
									case 1:
									case 2:
									case 3:
									case 4:
								}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.manager.ArgumentsUnregister) return e;
							var t = new l.manager.ArgumentsUnregister();
							switch (e.Reason) {
								case "UnknownUnregisterReason":
								case 0:
									t.Reason = 0;
									break;
								case "UnregisterPlaybackPaused":
								case 1:
									t.Reason = 1;
									break;
								case "UnregisterFinished":
								case 2:
									t.Reason = 2;
									break;
								case "UnregisterClosed":
								case 3:
									t.Reason = 3;
									break;
								case "UnregisterSwitching":
								case 4:
									t.Reason = 4;
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									(n.Reason =
										t.enums === String ? "UnknownUnregisterReason" : 0),
								null != e.Reason &&
									e.hasOwnProperty("Reason") &&
									(n.Reason =
										t.enums === String
											? l.manager.UnregisterReason[e.Reason]
											: e.Reason),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				o)),
				(e.exports = l);
		},
		function (e, t, n) {
			"use strict";
			var r,
				i,
				o,
				s = n(17),
				a = s.Reader,
				u = s.Writer,
				c = s.util,
				l = s.roots.default || (s.roots.default = {});
			(l.peers =
				(((o = {}).ArgumentsPingPong = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Seq = 0),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Seq &&
									e.hasOwnProperty("Seq") &&
									t.uint32(8).uint32(e.Seq),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.peers.ArgumentsPingPong();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Seq = e.uint32();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Seq &&
								  e.hasOwnProperty("Seq") &&
								  !c.isInteger(e.Seq)
								? "Seq: integer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.peers.ArgumentsPingPong) return e;
							var t = new l.peers.ArgumentsPingPong();
							return null != e.Seq && (t.Seq = e.Seq >>> 0), t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults && (n.Seq = 0),
								null != e.Seq && e.hasOwnProperty("Seq") && (n.Seq = e.Seq),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsSatisfy = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Resource = ""),
						(e.prototype.PartNumber = 0),
						(e.prototype.PartTotal = 0),
						(e.prototype.Content = c.newBuffer([])),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Resource &&
									e.hasOwnProperty("Resource") &&
									t.uint32(10).string(e.Resource),
								null != e.PartNumber &&
									e.hasOwnProperty("PartNumber") &&
									t.uint32(16).uint32(e.PartNumber),
								null != e.PartTotal &&
									e.hasOwnProperty("PartTotal") &&
									t.uint32(24).uint32(e.PartTotal),
								null != e.Content &&
									e.hasOwnProperty("Content") &&
									t.uint32(34).bytes(e.Content),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.peers.ArgumentsSatisfy();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Resource = e.string();
										break;
									case 2:
										r.PartNumber = e.uint32();
										break;
									case 3:
										r.PartTotal = e.uint32();
										break;
									case 4:
										r.Content = e.bytes();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Resource &&
								  e.hasOwnProperty("Resource") &&
								  !c.isString(e.Resource)
								? "Resource: string expected"
								: null != e.PartNumber &&
								  e.hasOwnProperty("PartNumber") &&
								  !c.isInteger(e.PartNumber)
								? "PartNumber: integer expected"
								: null != e.PartTotal &&
								  e.hasOwnProperty("PartTotal") &&
								  !c.isInteger(e.PartTotal)
								? "PartTotal: integer expected"
								: null != e.Content &&
								  e.hasOwnProperty("Content") &&
								  !(
										(e.Content && "number" == typeof e.Content.length) ||
										c.isString(e.Content)
								  )
								? "Content: buffer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.peers.ArgumentsSatisfy) return e;
							var t = new l.peers.ArgumentsSatisfy();
							return (
								null != e.Resource && (t.Resource = String(e.Resource)),
								null != e.PartNumber && (t.PartNumber = e.PartNumber >>> 0),
								null != e.PartTotal && (t.PartTotal = e.PartTotal >>> 0),
								null != e.Content &&
									("string" == typeof e.Content
										? c.base64.decode(
												e.Content,
												(t.Content = c.newBuffer(c.base64.length(e.Content))),
												0
										  )
										: e.Content.length && (t.Content = e.Content)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									((n.Resource = ""),
									(n.PartNumber = 0),
									(n.PartTotal = 0),
									t.bytes === String
										? (n.Content = "")
										: ((n.Content = []),
										  t.bytes !== Array &&
												(n.Content = c.newBuffer(n.Content)))),
								null != e.Resource &&
									e.hasOwnProperty("Resource") &&
									(n.Resource = e.Resource),
								null != e.PartNumber &&
									e.hasOwnProperty("PartNumber") &&
									(n.PartNumber = e.PartNumber),
								null != e.PartTotal &&
									e.hasOwnProperty("PartTotal") &&
									(n.PartTotal = e.PartTotal),
								null != e.Content &&
									e.hasOwnProperty("Content") &&
									(n.Content =
										t.bytes === String
											? c.base64.encode(e.Content, 0, e.Content.length)
											: t.bytes === Array
											? Array.prototype.slice.call(e.Content)
											: e.Content),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsAck = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.Resource = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Resource &&
									e.hasOwnProperty("Resource") &&
									t.uint32(10).string(e.Resource),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.peers.ArgumentsAck();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Resource = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.Resource &&
								  e.hasOwnProperty("Resource") &&
								  !c.isString(e.Resource)
								? "Resource: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.peers.ArgumentsAck) return e;
							var t = new l.peers.ArgumentsAck();
							return null != e.Resource && (t.Resource = String(e.Resource)), t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults && (n.Resource = ""),
								null != e.Resource &&
									e.hasOwnProperty("Resource") &&
									(n.Resource = e.Resource),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsResource = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.URL = ""),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.URL &&
									e.hasOwnProperty("URL") &&
									t.uint32(10).string(e.URL),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.peers.ArgumentsResource();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.URL = e.string();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.URL && e.hasOwnProperty("URL") && !c.isString(e.URL)
								? "URL: string expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.peers.ArgumentsResource) return e;
							var t = new l.peers.ArgumentsResource();
							return null != e.URL && (t.URL = String(e.URL)), t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults && (n.URL = ""),
								null != e.URL && e.hasOwnProperty("URL") && (n.URL = e.URL),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.ArgumentsPossession = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					return (
						(e.prototype.URLHashSet = c.newBuffer([])),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.URLHashSet &&
									e.hasOwnProperty("URLHashSet") &&
									t.uint32(10).bytes(e.URLHashSet),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.peers.ArgumentsPossession();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.URLHashSet = e.bytes();
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							return "object" != typeof e || null === e
								? "object expected"
								: null != e.URLHashSet &&
								  e.hasOwnProperty("URLHashSet") &&
								  !(
										(e.URLHashSet && "number" == typeof e.URLHashSet.length) ||
										c.isString(e.URLHashSet)
								  )
								? "URLHashSet: buffer expected"
								: null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.peers.ArgumentsPossession) return e;
							var t = new l.peers.ArgumentsPossession();
							return (
								null != e.URLHashSet &&
									("string" == typeof e.URLHashSet
										? c.base64.decode(
												e.URLHashSet,
												(t.URLHashSet = c.newBuffer(
													c.base64.length(e.URLHashSet)
												)),
												0
										  )
										: e.URLHashSet.length && (t.URLHashSet = e.URLHashSet)),
								t
							);
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									(t.bytes === String
										? (n.URLHashSet = "")
										: ((n.URLHashSet = []),
										  t.bytes !== Array &&
												(n.URLHashSet = c.newBuffer(n.URLHashSet)))),
								null != e.URLHashSet &&
									e.hasOwnProperty("URLHashSet") &&
									(n.URLHashSet =
										t.bytes === String
											? c.base64.encode(e.URLHashSet, 0, e.URLHashSet.length)
											: t.bytes === Array
											? Array.prototype.slice.call(e.URLHashSet)
											: e.URLHashSet),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				(o.MessageType =
					((r = {}),
					((i = Object.create(r))[(r[0] = "MessageTypePing")] = 0),
					(i[(r[257] = "MessageTypePong")] = 257),
					(i[(r[516] = "MessageTypePossession")] = 516),
					(i[(r[768] = "MessageTypeRequest")] = 768),
					(i[(r[769] = "MessageTypeSatisfy")] = 769),
					(i[(r[770] = "MessageTypeAck")] = 770),
					i)),
				(o.Message = (function () {
					function e(e) {
						if (e)
							for (var t = Object.keys(e), n = 0; n < t.length; ++n)
								null != e[t[n]] && (this[t[n]] = e[t[n]]);
					}
					var t;
					return (
						(e.prototype.Type = 0),
						(e.prototype.ArgumentsPingPong = null),
						(e.prototype.ArgumentsResource = null),
						(e.prototype.ArgumentsSatisfy = null),
						(e.prototype.ArgumentsPossession = null),
						(e.prototype.ArgumentsAck = null),
						Object.defineProperty(e.prototype, "Arguments", {
							get: c.oneOfGetter(
								(t = [
									"ArgumentsPingPong",
									"ArgumentsResource",
									"ArgumentsSatisfy",
									"ArgumentsPossession",
									"ArgumentsAck",
								])
							),
							set: c.oneOfSetter(t),
						}),
						(e.create = function (t) {
							return new e(t);
						}),
						(e.encode = function (e, t) {
							return (
								t || (t = u.create()),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									t.uint32(8).int32(e.Type),
								null != e.ArgumentsPingPong &&
									e.hasOwnProperty("ArgumentsPingPong") &&
									l.peers.ArgumentsPingPong.encode(
										e.ArgumentsPingPong,
										t.uint32(82).fork()
									).ldelim(),
								null != e.ArgumentsResource &&
									e.hasOwnProperty("ArgumentsResource") &&
									l.peers.ArgumentsResource.encode(
										e.ArgumentsResource,
										t.uint32(98).fork()
									).ldelim(),
								null != e.ArgumentsSatisfy &&
									e.hasOwnProperty("ArgumentsSatisfy") &&
									l.peers.ArgumentsSatisfy.encode(
										e.ArgumentsSatisfy,
										t.uint32(106).fork()
									).ldelim(),
								null != e.ArgumentsPossession &&
									e.hasOwnProperty("ArgumentsPossession") &&
									l.peers.ArgumentsPossession.encode(
										e.ArgumentsPossession,
										t.uint32(114).fork()
									).ldelim(),
								null != e.ArgumentsAck &&
									e.hasOwnProperty("ArgumentsAck") &&
									l.peers.ArgumentsAck.encode(
										e.ArgumentsAck,
										t.uint32(122).fork()
									).ldelim(),
								t
							);
						}),
						(e.encodeDelimited = function (e, t) {
							return this.encode(e, t).ldelim();
						}),
						(e.decode = function (e, t) {
							e instanceof a || (e = a.create(e));
							for (
								var n = void 0 === t ? e.len : e.pos + t,
									r = new l.peers.Message();
								e.pos < n;

							) {
								var i = e.uint32();
								switch (i >>> 3) {
									case 1:
										r.Type = e.int32();
										break;
									case 10:
										r.ArgumentsPingPong = l.peers.ArgumentsPingPong.decode(
											e,
											e.uint32()
										);
										break;
									case 12:
										r.ArgumentsResource = l.peers.ArgumentsResource.decode(
											e,
											e.uint32()
										);
										break;
									case 13:
										r.ArgumentsSatisfy = l.peers.ArgumentsSatisfy.decode(
											e,
											e.uint32()
										);
										break;
									case 14:
										r.ArgumentsPossession = l.peers.ArgumentsPossession.decode(
											e,
											e.uint32()
										);
										break;
									case 15:
										r.ArgumentsAck = l.peers.ArgumentsAck.decode(e, e.uint32());
										break;
									default:
										e.skipType(7 & i);
								}
							}
							return r;
						}),
						(e.decodeDelimited = function (e) {
							return (
								e instanceof a || (e = new a(e)), this.decode(e, e.uint32())
							);
						}),
						(e.verify = function (e) {
							if ("object" != typeof e || null === e) return "object expected";
							var t = {};
							if (null != e.Type && e.hasOwnProperty("Type"))
								switch (e.Type) {
									default:
										return "Type: enum value expected";
									case 0:
									case 257:
									case 516:
									case 768:
									case 769:
									case 770:
								}
							if (
								null != e.ArgumentsPingPong &&
								e.hasOwnProperty("ArgumentsPingPong") &&
								((t.Arguments = 1),
								(n = l.peers.ArgumentsPingPong.verify(e.ArgumentsPingPong)))
							)
								return "ArgumentsPingPong." + n;
							if (
								null != e.ArgumentsResource &&
								e.hasOwnProperty("ArgumentsResource")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.peers.ArgumentsResource.verify(e.ArgumentsResource)))
								)
									return "ArgumentsResource." + n;
							}
							if (
								null != e.ArgumentsSatisfy &&
								e.hasOwnProperty("ArgumentsSatisfy")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.peers.ArgumentsSatisfy.verify(e.ArgumentsSatisfy)))
								)
									return "ArgumentsSatisfy." + n;
							}
							if (
								null != e.ArgumentsPossession &&
								e.hasOwnProperty("ArgumentsPossession")
							) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								if (
									((t.Arguments = 1),
									(n = l.peers.ArgumentsPossession.verify(
										e.ArgumentsPossession
									)))
								)
									return "ArgumentsPossession." + n;
							}
							if (null != e.ArgumentsAck && e.hasOwnProperty("ArgumentsAck")) {
								if (1 === t.Arguments) return "Arguments: multiple values";
								var n;
								if (
									((t.Arguments = 1),
									(n = l.peers.ArgumentsAck.verify(e.ArgumentsAck)))
								)
									return "ArgumentsAck." + n;
							}
							return null;
						}),
						(e.fromObject = function (e) {
							if (e instanceof l.peers.Message) return e;
							var t = new l.peers.Message();
							switch (e.Type) {
								case "MessageTypePing":
								case 0:
									t.Type = 0;
									break;
								case "MessageTypePong":
								case 257:
									t.Type = 257;
									break;
								case "MessageTypePossession":
								case 516:
									t.Type = 516;
									break;
								case "MessageTypeRequest":
								case 768:
									t.Type = 768;
									break;
								case "MessageTypeSatisfy":
								case 769:
									t.Type = 769;
									break;
								case "MessageTypeAck":
								case 770:
									t.Type = 770;
							}
							if (null != e.ArgumentsPingPong) {
								if ("object" != typeof e.ArgumentsPingPong)
									throw TypeError(
										".peers.Message.ArgumentsPingPong: object expected"
									);
								t.ArgumentsPingPong = l.peers.ArgumentsPingPong.fromObject(
									e.ArgumentsPingPong
								);
							}
							if (null != e.ArgumentsResource) {
								if ("object" != typeof e.ArgumentsResource)
									throw TypeError(
										".peers.Message.ArgumentsResource: object expected"
									);
								t.ArgumentsResource = l.peers.ArgumentsResource.fromObject(
									e.ArgumentsResource
								);
							}
							if (null != e.ArgumentsSatisfy) {
								if ("object" != typeof e.ArgumentsSatisfy)
									throw TypeError(
										".peers.Message.ArgumentsSatisfy: object expected"
									);
								t.ArgumentsSatisfy = l.peers.ArgumentsSatisfy.fromObject(
									e.ArgumentsSatisfy
								);
							}
							if (null != e.ArgumentsPossession) {
								if ("object" != typeof e.ArgumentsPossession)
									throw TypeError(
										".peers.Message.ArgumentsPossession: object expected"
									);
								t.ArgumentsPossession = l.peers.ArgumentsPossession.fromObject(
									e.ArgumentsPossession
								);
							}
							if (null != e.ArgumentsAck) {
								if ("object" != typeof e.ArgumentsAck)
									throw TypeError(
										".peers.Message.ArgumentsAck: object expected"
									);
								t.ArgumentsAck = l.peers.ArgumentsAck.fromObject(
									e.ArgumentsAck
								);
							}
							return t;
						}),
						(e.toObject = function (e, t) {
							t || (t = {});
							var n = {};
							return (
								t.defaults &&
									(n.Type = t.enums === String ? "MessageTypePing" : 0),
								null != e.Type &&
									e.hasOwnProperty("Type") &&
									(n.Type =
										t.enums === String ? l.peers.MessageType[e.Type] : e.Type),
								null != e.ArgumentsPingPong &&
									e.hasOwnProperty("ArgumentsPingPong") &&
									((n.ArgumentsPingPong = l.peers.ArgumentsPingPong.toObject(
										e.ArgumentsPingPong,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsPingPong")),
								null != e.ArgumentsResource &&
									e.hasOwnProperty("ArgumentsResource") &&
									((n.ArgumentsResource = l.peers.ArgumentsResource.toObject(
										e.ArgumentsResource,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsResource")),
								null != e.ArgumentsSatisfy &&
									e.hasOwnProperty("ArgumentsSatisfy") &&
									((n.ArgumentsSatisfy = l.peers.ArgumentsSatisfy.toObject(
										e.ArgumentsSatisfy,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsSatisfy")),
								null != e.ArgumentsPossession &&
									e.hasOwnProperty("ArgumentsPossession") &&
									((n.ArgumentsPossession =
										l.peers.ArgumentsPossession.toObject(
											e.ArgumentsPossession,
											t
										)),
									t.oneofs && (n.Arguments = "ArgumentsPossession")),
								null != e.ArgumentsAck &&
									e.hasOwnProperty("ArgumentsAck") &&
									((n.ArgumentsAck = l.peers.ArgumentsAck.toObject(
										e.ArgumentsAck,
										t
									)),
									t.oneofs && (n.Arguments = "ArgumentsAck")),
								n
							);
						}),
						(e.prototype.toJSON = function () {
							return this.constructor.toObject(this, s.util.toJSONOptions);
						}),
						e
					);
				})()),
				o)),
				(e.exports = l);
		},
		function (e, t, n) {
			"use strict";
			(function (e) {
				/*!
				 * The buffer module from node.js, for the browser.
				 *
				 * @author   Feross Aboukhadijeh <http://feross.org>
				 * @license  MIT
				 */
				var r = n(41),
					i = n(42),
					o = n(43);
				function s() {
					return u.TYPED_ARRAY_SUPPORT ? 2147483647 : 1073741823;
				}
				function a(e, t) {
					if (s() < t) throw new RangeError("Invalid typed array length");
					return (
						u.TYPED_ARRAY_SUPPORT
							? ((e = new Uint8Array(t)).__proto__ = u.prototype)
							: (null === e && (e = new u(t)), (e.length = t)),
						e
					);
				}
				function u(e, t, n) {
					if (!(u.TYPED_ARRAY_SUPPORT || this instanceof u))
						return new u(e, t, n);
					if ("number" == typeof e) {
						if ("string" == typeof t)
							throw new Error(
								"If encoding is specified then the first argument must be a string"
							);
						return f(this, e);
					}
					return c(this, e, t, n);
				}
				function c(e, t, n, r) {
					if ("number" == typeof t)
						throw new TypeError('"value" argument must not be a number');
					return "undefined" != typeof ArrayBuffer && t instanceof ArrayBuffer
						? (function (e, t, n, r) {
								if ((t.byteLength, n < 0 || t.byteLength < n))
									throw new RangeError("'offset' is out of bounds");
								if (t.byteLength < n + (r || 0))
									throw new RangeError("'length' is out of bounds");
								t =
									void 0 === n && void 0 === r
										? new Uint8Array(t)
										: void 0 === r
										? new Uint8Array(t, n)
										: new Uint8Array(t, n, r);
								u.TYPED_ARRAY_SUPPORT
									? ((e = t).__proto__ = u.prototype)
									: (e = p(e, t));
								return e;
						  })(e, t, n, r)
						: "string" == typeof t
						? (function (e, t, n) {
								("string" == typeof n && "" !== n) || (n = "utf8");
								if (!u.isEncoding(n))
									throw new TypeError(
										'"encoding" must be a valid string encoding'
									);
								var r = 0 | g(t, n),
									i = (e = a(e, r)).write(t, n);
								i !== r && (e = e.slice(0, i));
								return e;
						  })(e, t, n)
						: (function (e, t) {
								if (u.isBuffer(t)) {
									var n = 0 | h(t.length);
									return 0 === (e = a(e, n)).length || t.copy(e, 0, 0, n), e;
								}
								if (t) {
									if (
										("undefined" != typeof ArrayBuffer &&
											t.buffer instanceof ArrayBuffer) ||
										"length" in t
									)
										return "number" != typeof t.length || (r = t.length) != r
											? a(e, 0)
											: p(e, t);
									if ("Buffer" === t.type && o(t.data)) return p(e, t.data);
								}
								var r;
								throw new TypeError(
									"First argument must be a string, Buffer, ArrayBuffer, Array, or array-like object."
								);
						  })(e, t);
				}
				function l(e) {
					if ("number" != typeof e)
						throw new TypeError('"size" argument must be a number');
					if (e < 0)
						throw new RangeError('"size" argument must not be negative');
				}
				function f(e, t) {
					if ((l(t), (e = a(e, t < 0 ? 0 : 0 | h(t))), !u.TYPED_ARRAY_SUPPORT))
						for (var n = 0; n < t; ++n) e[n] = 0;
					return e;
				}
				function p(e, t) {
					var n = t.length < 0 ? 0 : 0 | h(t.length);
					e = a(e, n);
					for (var r = 0; r < n; r += 1) e[r] = 255 & t[r];
					return e;
				}
				function h(e) {
					if (e >= s())
						throw new RangeError(
							"Attempt to allocate Buffer larger than maximum size: 0x" +
								s().toString(16) +
								" bytes"
						);
					return 0 | e;
				}
				function g(e, t) {
					if (u.isBuffer(e)) return e.length;
					if (
						"undefined" != typeof ArrayBuffer &&
						"function" == typeof ArrayBuffer.isView &&
						(ArrayBuffer.isView(e) || e instanceof ArrayBuffer)
					)
						return e.byteLength;
					"string" != typeof e && (e = "" + e);
					var n = e.length;
					if (0 === n) return 0;
					for (var r = !1; ; )
						switch (t) {
							case "ascii":
							case "latin1":
							case "binary":
								return n;
							case "utf8":
							case "utf-8":
							case void 0:
								return q(e).length;
							case "ucs2":
							case "ucs-2":
							case "utf16le":
							case "utf-16le":
								return 2 * n;
							case "hex":
								return n >>> 1;
							case "base64":
								return V(e).length;
							default:
								if (r) return q(e).length;
								(t = ("" + t).toLowerCase()), (r = !0);
						}
				}
				function d(e, t, n) {
					var r = !1;
					if (((void 0 === t || t < 0) && (t = 0), t > this.length)) return "";
					if (((void 0 === n || n > this.length) && (n = this.length), n <= 0))
						return "";
					if ((n >>>= 0) <= (t >>>= 0)) return "";
					for (e || (e = "utf8"); ; )
						switch (e) {
							case "hex":
								return M(this, t, n);
							case "utf8":
							case "utf-8":
								return C(this, t, n);
							case "ascii":
								return R(this, t, n);
							case "latin1":
							case "binary":
								return E(this, t, n);
							case "base64":
								return T(this, t, n);
							case "ucs2":
							case "ucs-2":
							case "utf16le":
							case "utf-16le":
								return L(this, t, n);
							default:
								if (r) throw new TypeError("Unknown encoding: " + e);
								(e = (e + "").toLowerCase()), (r = !0);
						}
				}
				function y(e, t, n) {
					var r = e[t];
					(e[t] = e[n]), (e[n] = r);
				}
				function m(e, t, n, r, i) {
					if (0 === e.length) return -1;
					if (
						("string" == typeof n
							? ((r = n), (n = 0))
							: n > 2147483647
							? (n = 2147483647)
							: n < -2147483648 && (n = -2147483648),
						(n = +n),
						isNaN(n) && (n = i ? 0 : e.length - 1),
						n < 0 && (n = e.length + n),
						n >= e.length)
					) {
						if (i) return -1;
						n = e.length - 1;
					} else if (n < 0) {
						if (!i) return -1;
						n = 0;
					}
					if (("string" == typeof t && (t = u.from(t, r)), u.isBuffer(t)))
						return 0 === t.length ? -1 : b(e, t, n, r, i);
					if ("number" == typeof t)
						return (
							(t &= 255),
							u.TYPED_ARRAY_SUPPORT &&
							"function" == typeof Uint8Array.prototype.indexOf
								? i
									? Uint8Array.prototype.indexOf.call(e, t, n)
									: Uint8Array.prototype.lastIndexOf.call(e, t, n)
								: b(e, [t], n, r, i)
						);
					throw new TypeError("val must be string, number or Buffer");
				}
				function b(e, t, n, r, i) {
					var o,
						s = 1,
						a = e.length,
						u = t.length;
					if (
						void 0 !== r &&
						("ucs2" === (r = String(r).toLowerCase()) ||
							"ucs-2" === r ||
							"utf16le" === r ||
							"utf-16le" === r)
					) {
						if (e.length < 2 || t.length < 2) return -1;
						(s = 2), (a /= 2), (u /= 2), (n /= 2);
					}
					function c(e, t) {
						return 1 === s ? e[t] : e.readUInt16BE(t * s);
					}
					if (i) {
						var l = -1;
						for (o = n; o < a; o++)
							if (c(e, o) === c(t, -1 === l ? 0 : o - l)) {
								if ((-1 === l && (l = o), o - l + 1 === u)) return l * s;
							} else -1 !== l && (o -= o - l), (l = -1);
					} else
						for (n + u > a && (n = a - u), o = n; o >= 0; o--) {
							for (var f = !0, p = 0; p < u; p++)
								if (c(e, o + p) !== c(t, p)) {
									f = !1;
									break;
								}
							if (f) return o;
						}
					return -1;
				}
				function w(e, t, n, r) {
					n = Number(n) || 0;
					var i = e.length - n;
					r ? (r = Number(r)) > i && (r = i) : (r = i);
					var o = t.length;
					if (o % 2 != 0) throw new TypeError("Invalid hex string");
					r > o / 2 && (r = o / 2);
					for (var s = 0; s < r; ++s) {
						var a = parseInt(t.substr(2 * s, 2), 16);
						if (isNaN(a)) return s;
						e[n + s] = a;
					}
					return s;
				}
				function S(e, t, n, r) {
					return F(q(t, e.length - n), e, n, r);
				}
				function P(e, t, n, r) {
					return F(
						(function (e) {
							for (var t = [], n = 0; n < e.length; ++n)
								t.push(255 & e.charCodeAt(n));
							return t;
						})(t),
						e,
						n,
						r
					);
				}
				function v(e, t, n, r) {
					return P(e, t, n, r);
				}
				function A(e, t, n, r) {
					return F(V(t), e, n, r);
				}
				function O(e, t, n, r) {
					return F(
						(function (e, t) {
							for (
								var n, r, i, o = [], s = 0;
								s < e.length && !((t -= 2) < 0);
								++s
							)
								(n = e.charCodeAt(s)),
									(r = n >> 8),
									(i = n % 256),
									o.push(i),
									o.push(r);
							return o;
						})(t, e.length - n),
						e,
						n,
						r
					);
				}
				function T(e, t, n) {
					return 0 === t && n === e.length
						? r.fromByteArray(e)
						: r.fromByteArray(e.slice(t, n));
				}
				function C(e, t, n) {
					n = Math.min(e.length, n);
					for (var r = [], i = t; i < n; ) {
						var o,
							s,
							a,
							u,
							c = e[i],
							l = null,
							f = c > 239 ? 4 : c > 223 ? 3 : c > 191 ? 2 : 1;
						if (i + f <= n)
							switch (f) {
								case 1:
									c < 128 && (l = c);
									break;
								case 2:
									128 == (192 & (o = e[i + 1])) &&
										(u = ((31 & c) << 6) | (63 & o)) > 127 &&
										(l = u);
									break;
								case 3:
									(o = e[i + 1]),
										(s = e[i + 2]),
										128 == (192 & o) &&
											128 == (192 & s) &&
											(u = ((15 & c) << 12) | ((63 & o) << 6) | (63 & s)) >
												2047 &&
											(u < 55296 || u > 57343) &&
											(l = u);
									break;
								case 4:
									(o = e[i + 1]),
										(s = e[i + 2]),
										(a = e[i + 3]),
										128 == (192 & o) &&
											128 == (192 & s) &&
											128 == (192 & a) &&
											(u =
												((15 & c) << 18) |
												((63 & o) << 12) |
												((63 & s) << 6) |
												(63 & a)) > 65535 &&
											u < 1114112 &&
											(l = u);
							}
						null === l
							? ((l = 65533), (f = 1))
							: l > 65535 &&
							  ((l -= 65536),
							  r.push(((l >>> 10) & 1023) | 55296),
							  (l = 56320 | (1023 & l))),
							r.push(l),
							(i += f);
					}
					return (function (e) {
						var t = e.length;
						if (t <= 4096) return String.fromCharCode.apply(String, e);
						var n = "",
							r = 0;
						for (; r < t; )
							n += String.fromCharCode.apply(String, e.slice(r, (r += 4096)));
						return n;
					})(r);
				}
				(t.Buffer = u),
					(t.SlowBuffer = function (e) {
						+e != e && (e = 0);
						return u.alloc(+e);
					}),
					(t.INSPECT_MAX_BYTES = 50),
					(u.TYPED_ARRAY_SUPPORT =
						void 0 !== e.TYPED_ARRAY_SUPPORT
							? e.TYPED_ARRAY_SUPPORT
							: (function () {
									try {
										var e = new Uint8Array(1);
										return (
											(e.__proto__ = {
												__proto__: Uint8Array.prototype,
												foo: function () {
													return 42;
												},
											}),
											42 === e.foo() &&
												"function" == typeof e.subarray &&
												0 === e.subarray(1, 1).byteLength
										);
									} catch (e) {
										return !1;
									}
							  })()),
					(t.kMaxLength = s()),
					(u.poolSize = 8192),
					(u._augment = function (e) {
						return (e.__proto__ = u.prototype), e;
					}),
					(u.from = function (e, t, n) {
						return c(null, e, t, n);
					}),
					u.TYPED_ARRAY_SUPPORT &&
						((u.prototype.__proto__ = Uint8Array.prototype),
						(u.__proto__ = Uint8Array),
						"undefined" != typeof Symbol &&
							Symbol.species &&
							u[Symbol.species] === u &&
							Object.defineProperty(u, Symbol.species, {
								value: null,
								configurable: !0,
							})),
					(u.alloc = function (e, t, n) {
						return (function (e, t, n, r) {
							return (
								l(t),
								t <= 0
									? a(e, t)
									: void 0 !== n
									? "string" == typeof r
										? a(e, t).fill(n, r)
										: a(e, t).fill(n)
									: a(e, t)
							);
						})(null, e, t, n);
					}),
					(u.allocUnsafe = function (e) {
						return f(null, e);
					}),
					(u.allocUnsafeSlow = function (e) {
						return f(null, e);
					}),
					(u.isBuffer = function (e) {
						return !(null == e || !e._isBuffer);
					}),
					(u.compare = function (e, t) {
						if (!u.isBuffer(e) || !u.isBuffer(t))
							throw new TypeError("Arguments must be Buffers");
						if (e === t) return 0;
						for (
							var n = e.length, r = t.length, i = 0, o = Math.min(n, r);
							i < o;
							++i
						)
							if (e[i] !== t[i]) {
								(n = e[i]), (r = t[i]);
								break;
							}
						return n < r ? -1 : r < n ? 1 : 0;
					}),
					(u.isEncoding = function (e) {
						switch (String(e).toLowerCase()) {
							case "hex":
							case "utf8":
							case "utf-8":
							case "ascii":
							case "latin1":
							case "binary":
							case "base64":
							case "ucs2":
							case "ucs-2":
							case "utf16le":
							case "utf-16le":
								return !0;
							default:
								return !1;
						}
					}),
					(u.concat = function (e, t) {
						if (!o(e))
							throw new TypeError(
								'"list" argument must be an Array of Buffers'
							);
						if (0 === e.length) return u.alloc(0);
						var n;
						if (void 0 === t)
							for (t = 0, n = 0; n < e.length; ++n) t += e[n].length;
						var r = u.allocUnsafe(t),
							i = 0;
						for (n = 0; n < e.length; ++n) {
							var s = e[n];
							if (!u.isBuffer(s))
								throw new TypeError(
									'"list" argument must be an Array of Buffers'
								);
							s.copy(r, i), (i += s.length);
						}
						return r;
					}),
					(u.byteLength = g),
					(u.prototype._isBuffer = !0),
					(u.prototype.swap16 = function () {
						var e = this.length;
						if (e % 2 != 0)
							throw new RangeError("Buffer size must be a multiple of 16-bits");
						for (var t = 0; t < e; t += 2) y(this, t, t + 1);
						return this;
					}),
					(u.prototype.swap32 = function () {
						var e = this.length;
						if (e % 4 != 0)
							throw new RangeError("Buffer size must be a multiple of 32-bits");
						for (var t = 0; t < e; t += 4)
							y(this, t, t + 3), y(this, t + 1, t + 2);
						return this;
					}),
					(u.prototype.swap64 = function () {
						var e = this.length;
						if (e % 8 != 0)
							throw new RangeError("Buffer size must be a multiple of 64-bits");
						for (var t = 0; t < e; t += 8)
							y(this, t, t + 7),
								y(this, t + 1, t + 6),
								y(this, t + 2, t + 5),
								y(this, t + 3, t + 4);
						return this;
					}),
					(u.prototype.toString = function () {
						var e = 0 | this.length;
						return 0 === e
							? ""
							: 0 === arguments.length
							? C(this, 0, e)
							: d.apply(this, arguments);
					}),
					(u.prototype.equals = function (e) {
						if (!u.isBuffer(e))
							throw new TypeError("Argument must be a Buffer");
						return this === e || 0 === u.compare(this, e);
					}),
					(u.prototype.inspect = function () {
						var e = "",
							n = t.INSPECT_MAX_BYTES;
						return (
							this.length > 0 &&
								((e = this.toString("hex", 0, n).match(/.{2}/g).join(" ")),
								this.length > n && (e += " ... ")),
							"<Buffer " + e + ">"
						);
					}),
					(u.prototype.compare = function (e, t, n, r, i) {
						if (!u.isBuffer(e))
							throw new TypeError("Argument must be a Buffer");
						if (
							(void 0 === t && (t = 0),
							void 0 === n && (n = e ? e.length : 0),
							void 0 === r && (r = 0),
							void 0 === i && (i = this.length),
							t < 0 || n > e.length || r < 0 || i > this.length)
						)
							throw new RangeError("out of range index");
						if (r >= i && t >= n) return 0;
						if (r >= i) return -1;
						if (t >= n) return 1;
						if (this === e) return 0;
						for (
							var o = (i >>>= 0) - (r >>>= 0),
								s = (n >>>= 0) - (t >>>= 0),
								a = Math.min(o, s),
								c = this.slice(r, i),
								l = e.slice(t, n),
								f = 0;
							f < a;
							++f
						)
							if (c[f] !== l[f]) {
								(o = c[f]), (s = l[f]);
								break;
							}
						return o < s ? -1 : s < o ? 1 : 0;
					}),
					(u.prototype.includes = function (e, t, n) {
						return -1 !== this.indexOf(e, t, n);
					}),
					(u.prototype.indexOf = function (e, t, n) {
						return m(this, e, t, n, !0);
					}),
					(u.prototype.lastIndexOf = function (e, t, n) {
						return m(this, e, t, n, !1);
					}),
					(u.prototype.write = function (e, t, n, r) {
						if (void 0 === t) (r = "utf8"), (n = this.length), (t = 0);
						else if (void 0 === n && "string" == typeof t)
							(r = t), (n = this.length), (t = 0);
						else {
							if (!isFinite(t))
								throw new Error(
									"Buffer.write(string, encoding, offset[, length]) is no longer supported"
								);
							(t |= 0),
								isFinite(n)
									? ((n |= 0), void 0 === r && (r = "utf8"))
									: ((r = n), (n = void 0));
						}
						var i = this.length - t;
						if (
							((void 0 === n || n > i) && (n = i),
							(e.length > 0 && (n < 0 || t < 0)) || t > this.length)
						)
							throw new RangeError("Attempt to write outside buffer bounds");
						r || (r = "utf8");
						for (var o = !1; ; )
							switch (r) {
								case "hex":
									return w(this, e, t, n);
								case "utf8":
								case "utf-8":
									return S(this, e, t, n);
								case "ascii":
									return P(this, e, t, n);
								case "latin1":
								case "binary":
									return v(this, e, t, n);
								case "base64":
									return A(this, e, t, n);
								case "ucs2":
								case "ucs-2":
								case "utf16le":
								case "utf-16le":
									return O(this, e, t, n);
								default:
									if (o) throw new TypeError("Unknown encoding: " + r);
									(r = ("" + r).toLowerCase()), (o = !0);
							}
					}),
					(u.prototype.toJSON = function () {
						return {
							type: "Buffer",
							data: Array.prototype.slice.call(this._arr || this, 0),
						};
					});
				function R(e, t, n) {
					var r = "";
					n = Math.min(e.length, n);
					for (var i = t; i < n; ++i) r += String.fromCharCode(127 & e[i]);
					return r;
				}
				function E(e, t, n) {
					var r = "";
					n = Math.min(e.length, n);
					for (var i = t; i < n; ++i) r += String.fromCharCode(e[i]);
					return r;
				}
				function M(e, t, n) {
					var r = e.length;
					(!t || t < 0) && (t = 0), (!n || n < 0 || n > r) && (n = r);
					for (var i = "", o = t; o < n; ++o) i += _(e[o]);
					return i;
				}
				function L(e, t, n) {
					for (var r = e.slice(t, n), i = "", o = 0; o < r.length; o += 2)
						i += String.fromCharCode(r[o] + 256 * r[o + 1]);
					return i;
				}
				function x(e, t, n) {
					if (e % 1 != 0 || e < 0) throw new RangeError("offset is not uint");
					if (e + t > n)
						throw new RangeError("Trying to access beyond buffer length");
				}
				function D(e, t, n, r, i, o) {
					if (!u.isBuffer(e))
						throw new TypeError('"buffer" argument must be a Buffer instance');
					if (t > i || t < o)
						throw new RangeError('"value" argument is out of bounds');
					if (n + r > e.length) throw new RangeError("Index out of range");
				}
				function I(e, t, n, r) {
					t < 0 && (t = 65535 + t + 1);
					for (var i = 0, o = Math.min(e.length - n, 2); i < o; ++i)
						e[n + i] =
							(t & (255 << (8 * (r ? i : 1 - i)))) >>> (8 * (r ? i : 1 - i));
				}
				function k(e, t, n, r) {
					t < 0 && (t = 4294967295 + t + 1);
					for (var i = 0, o = Math.min(e.length - n, 4); i < o; ++i)
						e[n + i] = (t >>> (8 * (r ? i : 3 - i))) & 255;
				}
				function j(e, t, n, r, i, o) {
					if (n + r > e.length) throw new RangeError("Index out of range");
					if (n < 0) throw new RangeError("Index out of range");
				}
				function B(e, t, n, r, o) {
					return o || j(e, 0, n, 4), i.write(e, t, n, r, 23, 4), n + 4;
				}
				function N(e, t, n, r, o) {
					return o || j(e, 0, n, 8), i.write(e, t, n, r, 52, 8), n + 8;
				}
				(u.prototype.slice = function (e, t) {
					var n,
						r = this.length;
					if (
						((e = ~~e) < 0 ? (e += r) < 0 && (e = 0) : e > r && (e = r),
						(t = void 0 === t ? r : ~~t) < 0
							? (t += r) < 0 && (t = 0)
							: t > r && (t = r),
						t < e && (t = e),
						u.TYPED_ARRAY_SUPPORT)
					)
						(n = this.subarray(e, t)).__proto__ = u.prototype;
					else {
						var i = t - e;
						n = new u(i, void 0);
						for (var o = 0; o < i; ++o) n[o] = this[o + e];
					}
					return n;
				}),
					(u.prototype.readUIntLE = function (e, t, n) {
						(e |= 0), (t |= 0), n || x(e, t, this.length);
						for (var r = this[e], i = 1, o = 0; ++o < t && (i *= 256); )
							r += this[e + o] * i;
						return r;
					}),
					(u.prototype.readUIntBE = function (e, t, n) {
						(e |= 0), (t |= 0), n || x(e, t, this.length);
						for (var r = this[e + --t], i = 1; t > 0 && (i *= 256); )
							r += this[e + --t] * i;
						return r;
					}),
					(u.prototype.readUInt8 = function (e, t) {
						return t || x(e, 1, this.length), this[e];
					}),
					(u.prototype.readUInt16LE = function (e, t) {
						return t || x(e, 2, this.length), this[e] | (this[e + 1] << 8);
					}),
					(u.prototype.readUInt16BE = function (e, t) {
						return t || x(e, 2, this.length), (this[e] << 8) | this[e + 1];
					}),
					(u.prototype.readUInt32LE = function (e, t) {
						return (
							t || x(e, 4, this.length),
							(this[e] | (this[e + 1] << 8) | (this[e + 2] << 16)) +
								16777216 * this[e + 3]
						);
					}),
					(u.prototype.readUInt32BE = function (e, t) {
						return (
							t || x(e, 4, this.length),
							16777216 * this[e] +
								((this[e + 1] << 16) | (this[e + 2] << 8) | this[e + 3])
						);
					}),
					(u.prototype.readIntLE = function (e, t, n) {
						(e |= 0), (t |= 0), n || x(e, t, this.length);
						for (var r = this[e], i = 1, o = 0; ++o < t && (i *= 256); )
							r += this[e + o] * i;
						return r >= (i *= 128) && (r -= Math.pow(2, 8 * t)), r;
					}),
					(u.prototype.readIntBE = function (e, t, n) {
						(e |= 0), (t |= 0), n || x(e, t, this.length);
						for (var r = t, i = 1, o = this[e + --r]; r > 0 && (i *= 256); )
							o += this[e + --r] * i;
						return o >= (i *= 128) && (o -= Math.pow(2, 8 * t)), o;
					}),
					(u.prototype.readInt8 = function (e, t) {
						return (
							t || x(e, 1, this.length),
							128 & this[e] ? -1 * (255 - this[e] + 1) : this[e]
						);
					}),
					(u.prototype.readInt16LE = function (e, t) {
						t || x(e, 2, this.length);
						var n = this[e] | (this[e + 1] << 8);
						return 32768 & n ? 4294901760 | n : n;
					}),
					(u.prototype.readInt16BE = function (e, t) {
						t || x(e, 2, this.length);
						var n = this[e + 1] | (this[e] << 8);
						return 32768 & n ? 4294901760 | n : n;
					}),
					(u.prototype.readInt32LE = function (e, t) {
						return (
							t || x(e, 4, this.length),
							this[e] |
								(this[e + 1] << 8) |
								(this[e + 2] << 16) |
								(this[e + 3] << 24)
						);
					}),
					(u.prototype.readInt32BE = function (e, t) {
						return (
							t || x(e, 4, this.length),
							(this[e] << 24) |
								(this[e + 1] << 16) |
								(this[e + 2] << 8) |
								this[e + 3]
						);
					}),
					(u.prototype.readFloatLE = function (e, t) {
						return t || x(e, 4, this.length), i.read(this, e, !0, 23, 4);
					}),
					(u.prototype.readFloatBE = function (e, t) {
						return t || x(e, 4, this.length), i.read(this, e, !1, 23, 4);
					}),
					(u.prototype.readDoubleLE = function (e, t) {
						return t || x(e, 8, this.length), i.read(this, e, !0, 52, 8);
					}),
					(u.prototype.readDoubleBE = function (e, t) {
						return t || x(e, 8, this.length), i.read(this, e, !1, 52, 8);
					}),
					(u.prototype.writeUIntLE = function (e, t, n, r) {
						((e = +e), (t |= 0), (n |= 0), r) ||
							D(this, e, t, n, Math.pow(2, 8 * n) - 1, 0);
						var i = 1,
							o = 0;
						for (this[t] = 255 & e; ++o < n && (i *= 256); )
							this[t + o] = (e / i) & 255;
						return t + n;
					}),
					(u.prototype.writeUIntBE = function (e, t, n, r) {
						((e = +e), (t |= 0), (n |= 0), r) ||
							D(this, e, t, n, Math.pow(2, 8 * n) - 1, 0);
						var i = n - 1,
							o = 1;
						for (this[t + i] = 255 & e; --i >= 0 && (o *= 256); )
							this[t + i] = (e / o) & 255;
						return t + n;
					}),
					(u.prototype.writeUInt8 = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 1, 255, 0),
							u.TYPED_ARRAY_SUPPORT || (e = Math.floor(e)),
							(this[t] = 255 & e),
							t + 1
						);
					}),
					(u.prototype.writeUInt16LE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 2, 65535, 0),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = 255 & e), (this[t + 1] = e >>> 8))
								: I(this, e, t, !0),
							t + 2
						);
					}),
					(u.prototype.writeUInt16BE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 2, 65535, 0),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = e >>> 8), (this[t + 1] = 255 & e))
								: I(this, e, t, !1),
							t + 2
						);
					}),
					(u.prototype.writeUInt32LE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 4, 4294967295, 0),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t + 3] = e >>> 24),
								  (this[t + 2] = e >>> 16),
								  (this[t + 1] = e >>> 8),
								  (this[t] = 255 & e))
								: k(this, e, t, !0),
							t + 4
						);
					}),
					(u.prototype.writeUInt32BE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 4, 4294967295, 0),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = e >>> 24),
								  (this[t + 1] = e >>> 16),
								  (this[t + 2] = e >>> 8),
								  (this[t + 3] = 255 & e))
								: k(this, e, t, !1),
							t + 4
						);
					}),
					(u.prototype.writeIntLE = function (e, t, n, r) {
						if (((e = +e), (t |= 0), !r)) {
							var i = Math.pow(2, 8 * n - 1);
							D(this, e, t, n, i - 1, -i);
						}
						var o = 0,
							s = 1,
							a = 0;
						for (this[t] = 255 & e; ++o < n && (s *= 256); )
							e < 0 && 0 === a && 0 !== this[t + o - 1] && (a = 1),
								(this[t + o] = (((e / s) >> 0) - a) & 255);
						return t + n;
					}),
					(u.prototype.writeIntBE = function (e, t, n, r) {
						if (((e = +e), (t |= 0), !r)) {
							var i = Math.pow(2, 8 * n - 1);
							D(this, e, t, n, i - 1, -i);
						}
						var o = n - 1,
							s = 1,
							a = 0;
						for (this[t + o] = 255 & e; --o >= 0 && (s *= 256); )
							e < 0 && 0 === a && 0 !== this[t + o + 1] && (a = 1),
								(this[t + o] = (((e / s) >> 0) - a) & 255);
						return t + n;
					}),
					(u.prototype.writeInt8 = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 1, 127, -128),
							u.TYPED_ARRAY_SUPPORT || (e = Math.floor(e)),
							e < 0 && (e = 255 + e + 1),
							(this[t] = 255 & e),
							t + 1
						);
					}),
					(u.prototype.writeInt16LE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 2, 32767, -32768),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = 255 & e), (this[t + 1] = e >>> 8))
								: I(this, e, t, !0),
							t + 2
						);
					}),
					(u.prototype.writeInt16BE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 2, 32767, -32768),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = e >>> 8), (this[t + 1] = 255 & e))
								: I(this, e, t, !1),
							t + 2
						);
					}),
					(u.prototype.writeInt32LE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 4, 2147483647, -2147483648),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = 255 & e),
								  (this[t + 1] = e >>> 8),
								  (this[t + 2] = e >>> 16),
								  (this[t + 3] = e >>> 24))
								: k(this, e, t, !0),
							t + 4
						);
					}),
					(u.prototype.writeInt32BE = function (e, t, n) {
						return (
							(e = +e),
							(t |= 0),
							n || D(this, e, t, 4, 2147483647, -2147483648),
							e < 0 && (e = 4294967295 + e + 1),
							u.TYPED_ARRAY_SUPPORT
								? ((this[t] = e >>> 24),
								  (this[t + 1] = e >>> 16),
								  (this[t + 2] = e >>> 8),
								  (this[t + 3] = 255 & e))
								: k(this, e, t, !1),
							t + 4
						);
					}),
					(u.prototype.writeFloatLE = function (e, t, n) {
						return B(this, e, t, !0, n);
					}),
					(u.prototype.writeFloatBE = function (e, t, n) {
						return B(this, e, t, !1, n);
					}),
					(u.prototype.writeDoubleLE = function (e, t, n) {
						return N(this, e, t, !0, n);
					}),
					(u.prototype.writeDoubleBE = function (e, t, n) {
						return N(this, e, t, !1, n);
					}),
					(u.prototype.copy = function (e, t, n, r) {
						if (
							(n || (n = 0),
							r || 0 === r || (r = this.length),
							t >= e.length && (t = e.length),
							t || (t = 0),
							r > 0 && r < n && (r = n),
							r === n)
						)
							return 0;
						if (0 === e.length || 0 === this.length) return 0;
						if (t < 0) throw new RangeError("targetStart out of bounds");
						if (n < 0 || n >= this.length)
							throw new RangeError("sourceStart out of bounds");
						if (r < 0) throw new RangeError("sourceEnd out of bounds");
						r > this.length && (r = this.length),
							e.length - t < r - n && (r = e.length - t + n);
						var i,
							o = r - n;
						if (this === e && n < t && t < r)
							for (i = o - 1; i >= 0; --i) e[i + t] = this[i + n];
						else if (o < 1e3 || !u.TYPED_ARRAY_SUPPORT)
							for (i = 0; i < o; ++i) e[i + t] = this[i + n];
						else Uint8Array.prototype.set.call(e, this.subarray(n, n + o), t);
						return o;
					}),
					(u.prototype.fill = function (e, t, n, r) {
						if ("string" == typeof e) {
							if (
								("string" == typeof t
									? ((r = t), (t = 0), (n = this.length))
									: "string" == typeof n && ((r = n), (n = this.length)),
								1 === e.length)
							) {
								var i = e.charCodeAt(0);
								i < 256 && (e = i);
							}
							if (void 0 !== r && "string" != typeof r)
								throw new TypeError("encoding must be a string");
							if ("string" == typeof r && !u.isEncoding(r))
								throw new TypeError("Unknown encoding: " + r);
						} else "number" == typeof e && (e &= 255);
						if (t < 0 || this.length < t || this.length < n)
							throw new RangeError("Out of range index");
						if (n <= t) return this;
						var o;
						if (
							((t >>>= 0),
							(n = void 0 === n ? this.length : n >>> 0),
							e || (e = 0),
							"number" == typeof e)
						)
							for (o = t; o < n; ++o) this[o] = e;
						else {
							var s = u.isBuffer(e) ? e : q(new u(e, r).toString()),
								a = s.length;
							for (o = 0; o < n - t; ++o) this[o + t] = s[o % a];
						}
						return this;
					});
				var U = /[^+\/0-9A-Za-z-_]/g;
				function _(e) {
					return e < 16 ? "0" + e.toString(16) : e.toString(16);
				}
				function q(e, t) {
					var n;
					t = t || 1 / 0;
					for (var r = e.length, i = null, o = [], s = 0; s < r; ++s) {
						if ((n = e.charCodeAt(s)) > 55295 && n < 57344) {
							if (!i) {
								if (n > 56319) {
									(t -= 3) > -1 && o.push(239, 191, 189);
									continue;
								}
								if (s + 1 === r) {
									(t -= 3) > -1 && o.push(239, 191, 189);
									continue;
								}
								i = n;
								continue;
							}
							if (n < 56320) {
								(t -= 3) > -1 && o.push(239, 191, 189), (i = n);
								continue;
							}
							n = 65536 + (((i - 55296) << 10) | (n - 56320));
						} else i && (t -= 3) > -1 && o.push(239, 191, 189);
						if (((i = null), n < 128)) {
							if ((t -= 1) < 0) break;
							o.push(n);
						} else if (n < 2048) {
							if ((t -= 2) < 0) break;
							o.push((n >> 6) | 192, (63 & n) | 128);
						} else if (n < 65536) {
							if ((t -= 3) < 0) break;
							o.push((n >> 12) | 224, ((n >> 6) & 63) | 128, (63 & n) | 128);
						} else {
							if (!(n < 1114112)) throw new Error("Invalid code point");
							if ((t -= 4) < 0) break;
							o.push(
								(n >> 18) | 240,
								((n >> 12) & 63) | 128,
								((n >> 6) & 63) | 128,
								(63 & n) | 128
							);
						}
					}
					return o;
				}
				function V(e) {
					return r.toByteArray(
						(function (e) {
							if (
								(e = (function (e) {
									return e.trim ? e.trim() : e.replace(/^\s+|\s+$/g, "");
								})(e).replace(U, "")).length < 2
							)
								return "";
							for (; e.length % 4 != 0; ) e += "=";
							return e;
						})(e)
					);
				}
				function F(e, t, n, r) {
					for (var i = 0; i < r && !(i + n >= t.length || i >= e.length); ++i)
						t[i + n] = e[i];
					return i;
				}
			}).call(this, n(10));
		},
		function (e, t, n) {
			(function (e, r) {
				var i;
				/*!
				 * Platform.js v1.3.6
				 * Copyright 2014-2020 Benjamin Tan
				 * Copyright 2011-2013 John-David Dalton
				 * Available under MIT license
				 */ (function () {
					"use strict";
					var o = { function: !0, object: !0 },
						s = (o[typeof window] && window) || this,
						a = o[typeof t] && t,
						u = o[typeof e] && e && !e.nodeType && e,
						c = a && u && "object" == typeof r && r;
					!c || (c.global !== c && c.window !== c && c.self !== c) || (s = c);
					var l = Math.pow(2, 53) - 1,
						f = /\bOpera/,
						p = Object.prototype,
						h = p.hasOwnProperty,
						g = p.toString;
					function d(e) {
						return (e = String(e)).charAt(0).toUpperCase() + e.slice(1);
					}
					function y(e) {
						return (e = P(e)), /^(?:webOS|i(?:OS|P))/.test(e) ? e : d(e);
					}
					function m(e, t) {
						for (var n in e) h.call(e, n) && t(e[n], n, e);
					}
					function b(e) {
						return null == e ? d(e) : g.call(e).slice(8, -1);
					}
					function w(e) {
						return String(e).replace(/([ -])(?!$)/g, "$1?");
					}
					function S(e, t) {
						var n = null;
						return (
							(function (e, t) {
								var n = -1,
									r = e ? e.length : 0;
								if ("number" == typeof r && r > -1 && r <= l)
									for (; ++n < r; ) t(e[n], n, e);
								else m(e, t);
							})(e, function (r, i) {
								n = t(n, r, i, e);
							}),
							n
						);
					}
					function P(e) {
						return String(e).replace(/^ +| +$/g, "");
					}
					var v = (function e(t) {
						var n = s,
							r = t && "object" == typeof t && "String" != b(t);
						r && ((n = t), (t = null));
						var i = n.navigator || {},
							o = i.userAgent || "";
						t || (t = o);
						var a,
							u,
							c,
							l,
							p,
							h = r
								? !!i.likeChrome
								: /\bChrome\b/.test(t) && !/internal|\n/i.test(g.toString()),
							d = r ? "Object" : "ScriptBridgingProxyObject",
							v = r ? "Object" : "Environment",
							A = r && n.java ? "JavaPackage" : b(n.java),
							O = r ? "Object" : "RuntimeObject",
							T = /\bJava/.test(A) && n.java,
							C = T && b(n.environment) == v,
							R = T ? "a" : "Î±",
							E = T ? "b" : "Î²",
							M = n.document || {},
							L = n.operamini || n.opera,
							x = f.test((x = r && L ? L["[[Class]]"] : b(L))) ? x : (L = null),
							D = t,
							I = [],
							k = null,
							j = t == o,
							B = j && L && "function" == typeof L.version && L.version(),
							N = S(
								[
									{ label: "EdgeHTML", pattern: "Edge" },
									"Trident",
									{ label: "WebKit", pattern: "AppleWebKit" },
									"iCab",
									"Presto",
									"NetFront",
									"Tasman",
									"KHTML",
									"Gecko",
								],
								function (e, n) {
									return (
										e ||
										(RegExp("\\b" + (n.pattern || w(n)) + "\\b", "i").exec(t) &&
											(n.label || n))
									);
								}
							),
							U = (function (e) {
								return S(e, function (e, n) {
									return (
										e ||
										(RegExp("\\b" + (n.pattern || w(n)) + "\\b", "i").exec(t) &&
											(n.label || n))
									);
								});
							})([
								"Adobe AIR",
								"Arora",
								"Avant Browser",
								"Breach",
								"Camino",
								"Electron",
								"Epiphany",
								"Fennec",
								"Flock",
								"Galeon",
								"GreenBrowser",
								"iCab",
								"Iceweasel",
								"K-Meleon",
								"Konqueror",
								"Lunascape",
								"Maxthon",
								{
									label: "Microsoft Edge",
									pattern: "(?:Edge|Edg|EdgA|EdgiOS)",
								},
								"Midori",
								"Nook Browser",
								"PaleMoon",
								"PhantomJS",
								"Raven",
								"Rekonq",
								"RockMelt",
								{ label: "Samsung Internet", pattern: "SamsungBrowser" },
								"SeaMonkey",
								{ label: "Silk", pattern: "(?:Cloud9|Silk-Accelerated)" },
								"Sleipnir",
								"SlimBrowser",
								{ label: "SRWare Iron", pattern: "Iron" },
								"Sunrise",
								"Swiftfox",
								"Vivaldi",
								"Waterfox",
								"WebPositive",
								{ label: "Yandex Browser", pattern: "YaBrowser" },
								{ label: "UC Browser", pattern: "UCBrowser" },
								"Opera Mini",
								{ label: "Opera Mini", pattern: "OPiOS" },
								"Opera",
								{ label: "Opera", pattern: "OPR" },
								"Chromium",
								"Chrome",
								{ label: "Chrome", pattern: "(?:HeadlessChrome)" },
								{ label: "Chrome Mobile", pattern: "(?:CriOS|CrMo)" },
								{ label: "Firefox", pattern: "(?:Firefox|Minefield)" },
								{ label: "Firefox for iOS", pattern: "FxiOS" },
								{ label: "IE", pattern: "IEMobile" },
								{ label: "IE", pattern: "MSIE" },
								"Safari",
							]),
							_ = F([
								{ label: "BlackBerry", pattern: "BB10" },
								"BlackBerry",
								{ label: "Galaxy S", pattern: "GT-I9000" },
								{ label: "Galaxy S2", pattern: "GT-I9100" },
								{ label: "Galaxy S3", pattern: "GT-I9300" },
								{ label: "Galaxy S4", pattern: "GT-I9500" },
								{ label: "Galaxy S5", pattern: "SM-G900" },
								{ label: "Galaxy S6", pattern: "SM-G920" },
								{ label: "Galaxy S6 Edge", pattern: "SM-G925" },
								{ label: "Galaxy S7", pattern: "SM-G930" },
								{ label: "Galaxy S7 Edge", pattern: "SM-G935" },
								"Google TV",
								"Lumia",
								"iPad",
								"iPod",
								"iPhone",
								"Kindle",
								{
									label: "Kindle Fire",
									pattern: "(?:Cloud9|Silk-Accelerated)",
								},
								"Nexus",
								"Nook",
								"PlayBook",
								"PlayStation Vita",
								"PlayStation",
								"TouchPad",
								"Transformer",
								{ label: "Wii U", pattern: "WiiU" },
								"Wii",
								"Xbox One",
								{ label: "Xbox 360", pattern: "Xbox" },
								"Xoom",
							]),
							q = (function (e) {
								return S(e, function (e, n, r) {
									return (
										e ||
										((n[_] ||
											n[/^[a-z]+(?: +[a-z]+\b)*/i.exec(_)] ||
											RegExp("\\b" + w(r) + "(?:\\b|\\w*\\d)", "i").exec(t)) &&
											r)
									);
								});
							})({
								Apple: { iPad: 1, iPhone: 1, iPod: 1 },
								Alcatel: {},
								Archos: {},
								Amazon: { Kindle: 1, "Kindle Fire": 1 },
								Asus: { Transformer: 1 },
								"Barnes & Noble": { Nook: 1 },
								BlackBerry: { PlayBook: 1 },
								Google: { "Google TV": 1, Nexus: 1 },
								HP: { TouchPad: 1 },
								HTC: {},
								Huawei: {},
								Lenovo: {},
								LG: {},
								Microsoft: { Xbox: 1, "Xbox One": 1 },
								Motorola: { Xoom: 1 },
								Nintendo: { "Wii U": 1, Wii: 1 },
								Nokia: { Lumia: 1 },
								Oppo: {},
								Samsung: {
									"Galaxy S": 1,
									"Galaxy S2": 1,
									"Galaxy S3": 1,
									"Galaxy S4": 1,
								},
								Sony: { PlayStation: 1, "PlayStation Vita": 1 },
								Xiaomi: { Mi: 1, Redmi: 1 },
							}),
							V = (function (e) {
								return S(e, function (e, n) {
									var r = n.pattern || w(n);
									return (
										!e &&
											(e = RegExp(
												"\\b" + r + "(?:/[\\d.]+|[ \\w.]*)",
												"i"
											).exec(t)) &&
											(e = (function (e, t, n) {
												var r = {
													"10.0": "10",
													6.4: "10 Technical Preview",
													6.3: "8.1",
													6.2: "8",
													6.1: "Server 2008 R2 / 7",
													"6.0": "Server 2008 / Vista",
													5.2: "Server 2003 / XP 64-bit",
													5.1: "XP",
													5.01: "2000 SP1",
													"5.0": "2000",
													"4.0": "NT",
													"4.90": "ME",
												};
												return (
													t &&
														n &&
														/^Win/i.test(e) &&
														!/^Windows Phone /i.test(e) &&
														(r = r[/[\d.]+$/.exec(e)]) &&
														(e = "Windows " + r),
													(e = String(e)),
													t && n && (e = e.replace(RegExp(t, "i"), n)),
													(e = y(
														e
															.replace(/ ce$/i, " CE")
															.replace(/\bhpw/i, "web")
															.replace(/\bMacintosh\b/, "Mac OS")
															.replace(/_PowerPC\b/i, " OS")
															.replace(/\b(OS X) [^ \d]+/i, "$1")
															.replace(/\bMac (OS X)\b/, "$1")
															.replace(/\/(\d)/, " $1")
															.replace(/_/g, ".")
															.replace(/(?: BePC|[ .]*fc[ \d.]+)$/i, "")
															.replace(/\bx86\.64\b/gi, "x86_64")
															.replace(/\b(Windows Phone) OS\b/, "$1")
															.replace(/\b(Chrome OS \w+) [\d.]+\b/, "$1")
															.split(" on ")[0]
													))
												);
											})(e, r, n.label || n)),
										e
									);
								});
							})([
								"Windows Phone",
								"KaiOS",
								"Android",
								"CentOS",
								{ label: "Chrome OS", pattern: "CrOS" },
								"Debian",
								{ label: "DragonFly BSD", pattern: "DragonFly" },
								"Fedora",
								"FreeBSD",
								"Gentoo",
								"Haiku",
								"Kubuntu",
								"Linux Mint",
								"OpenBSD",
								"Red Hat",
								"SuSE",
								"Ubuntu",
								"Xubuntu",
								"Cygwin",
								"Symbian OS",
								"hpwOS",
								"webOS ",
								"webOS",
								"Tablet OS",
								"Tizen",
								"Linux",
								"Mac OS X",
								"Macintosh",
								"Mac",
								"Windows 98;",
								"Windows ",
							]);
						function F(e) {
							return S(e, function (e, n) {
								var r = n.pattern || w(n);
								return (
									!e &&
										(e =
											RegExp("\\b" + r + " *\\d+[.\\w_]*", "i").exec(t) ||
											RegExp("\\b" + r + " *\\w+-[\\w]*", "i").exec(t) ||
											RegExp(
												"\\b" +
													r +
													"(?:; *(?:[a-z]+[_-])?[a-z]+\\d+|[^ ();-]*)",
												"i"
											).exec(t)) &&
										((e = String(
											n.label && !RegExp(r, "i").test(n.label) ? n.label : e
										).split("/"))[1] &&
											!/[\d.]+/.test(e[0]) &&
											(e[0] += " " + e[1]),
										(n = n.label || n),
										(e = y(
											e[0]
												.replace(RegExp(r, "i"), n)
												.replace(RegExp("; *(?:" + n + "[_-])?", "i"), " ")
												.replace(RegExp("(" + n + ")[-_.]?(\\w)", "i"), "$1 $2")
										))),
									e
								);
							});
						}
						function z(e) {
							return S(e, function (e, n) {
								return (
									e ||
									(RegExp(
										n +
											"(?:-[\\d.]+/|(?: for [\\w-]+)?[ /-])([\\d.]+[^ ();/_-]*)",
										"i"
									).exec(t) || 0)[1] ||
									null
								);
							});
						}
						if (
							(N && (N = [N]),
							/\bAndroid\b/.test(V) &&
								!_ &&
								(a = /\bAndroid[^;]*;(.*?)(?:Build|\) AppleWebKit)\b/i.exec(
									t
								)) &&
								(_ = P(a[1]).replace(/^[a-z]{2}-[a-z]{2};\s*/i, "") || null),
							q && !_
								? (_ = F([q]))
								: q &&
								  _ &&
								  (_ = _.replace(
										RegExp("^(" + w(q) + ")[-_.\\s]", "i"),
										q + " "
								  ).replace(
										RegExp("^(" + w(q) + ")[-_.]?(\\w)", "i"),
										q + " $2"
								  )),
							(a = /\bGoogle TV\b/.exec(_)) && (_ = a[0]),
							/\bSimulator\b/i.test(t) &&
								(_ = (_ ? _ + " " : "") + "Simulator"),
							"Opera Mini" == U &&
								/\bOPiOS\b/.test(t) &&
								I.push("running in Turbo/Uncompressed mode"),
							"IE" == U && /\blike iPhone OS\b/.test(t)
								? ((q = (a = e(t.replace(/like iPhone OS/, ""))).manufacturer),
								  (_ = a.product))
								: /^iP/.test(_)
								? (U || (U = "Safari"),
								  (V =
										"iOS" +
										((a = / OS ([\d_]+)/i.exec(t))
											? " " + a[1].replace(/_/g, ".")
											: "")))
								: "Konqueror" == U && /^Linux\b/i.test(V)
								? (V = "Kubuntu")
								: (q &&
										"Google" != q &&
										((/Chrome/.test(U) && !/\bMobile Safari\b/i.test(t)) ||
											/\bVita\b/.test(_))) ||
								  (/\bAndroid\b/.test(V) &&
										/^Chrome/.test(U) &&
										/\bVersion\//i.test(t))
								? ((U = "Android Browser"),
								  (V = /\bAndroid\b/.test(V) ? V : "Android"))
								: "Silk" == U
								? (/\bMobi/i.test(t) ||
										((V = "Android"), I.unshift("desktop mode")),
								  /Accelerated *= *true/i.test(t) && I.unshift("accelerated"))
								: "UC Browser" == U && /\bUCWEB\b/.test(t)
								? I.push("speed mode")
								: "PaleMoon" == U && (a = /\bFirefox\/([\d.]+)\b/.exec(t))
								? I.push("identifying as Firefox " + a[1])
								: "Firefox" == U && (a = /\b(Mobile|Tablet|TV)\b/i.exec(t))
								? (V || (V = "Firefox OS"), _ || (_ = a[1]))
								: !U ||
								  (a =
										!/\bMinefield\b/i.test(t) &&
										/\b(?:Firefox|Safari)\b/.exec(U))
								? (U &&
										!_ &&
										/[\/,]|^[^(]+?\)/.test(t.slice(t.indexOf(a + "/") + 8)) &&
										(U = null),
								  (a = _ || q || V) &&
										(_ ||
											q ||
											/\b(?:Android|Symbian OS|Tablet OS|webOS)\b/.test(V)) &&
										(U =
											/[a-z]+(?: Hat)?/i.exec(/\bAndroid\b/.test(V) ? V : a) +
											" Browser"))
								: "Electron" == U &&
								  (a = (/\bChrome\/([\d.]+)\b/.exec(t) || 0)[1]) &&
								  I.push("Chromium " + a),
							B ||
								(B = z([
									"(?:Cloud9|CriOS|CrMo|Edge|Edg|EdgA|EdgiOS|FxiOS|HeadlessChrome|IEMobile|Iron|Opera ?Mini|OPiOS|OPR|Raven|SamsungBrowser|Silk(?!/[\\d.]+$)|UCBrowser|YaBrowser)",
									"Version",
									w(U),
									"(?:Firefox|Minefield|NetFront)",
								])),
							(a =
								("iCab" == N && parseFloat(B) > 3
									? "WebKit"
									: /\bOpera\b/.test(U) &&
									  (/\bOPR\b/.test(t) ? "Blink" : "Presto")) ||
								(/\b(?:Midori|Nook|Safari)\b/i.test(t) &&
									!/^(?:Trident|EdgeHTML)$/.test(N) &&
									"WebKit") ||
								(!N &&
									/\bMSIE\b/i.test(t) &&
									("Mac OS" == V ? "Tasman" : "Trident")) ||
								("WebKit" == N &&
									/\bPlayStation\b(?! Vita\b)/i.test(U) &&
									"NetFront")) && (N = [a]),
							"IE" == U && (a = (/; *(?:XBLWP|ZuneWP)(\d+)/i.exec(t) || 0)[1])
								? ((U += " Mobile"),
								  (V = "Windows Phone " + (/\+$/.test(a) ? a : a + ".x")),
								  I.unshift("desktop mode"))
								: /\bWPDesktop\b/i.test(t)
								? ((U = "IE Mobile"),
								  (V = "Windows Phone 8.x"),
								  I.unshift("desktop mode"),
								  B || (B = (/\brv:([\d.]+)/.exec(t) || 0)[1]))
								: "IE" != U &&
								  "Trident" == N &&
								  (a = /\brv:([\d.]+)/.exec(t)) &&
								  (U && I.push("identifying as " + U + (B ? " " + B : "")),
								  (U = "IE"),
								  (B = a[1])),
							j)
						) {
							if (
								((l = "global"),
								(p = null != (c = n) ? typeof c[l] : "number"),
								/^(?:boolean|number|string|undefined)$/.test(p) ||
									("object" == p && !c[l]))
							)
								b((a = n.runtime)) == d
									? ((U = "Adobe AIR"), (V = a.flash.system.Capabilities.os))
									: b((a = n.phantom)) == O
									? ((U = "PhantomJS"),
									  (B =
											(a = a.version || null) &&
											a.major + "." + a.minor + "." + a.patch))
									: "number" == typeof M.documentMode &&
									  (a = /\bTrident\/(\d+)/i.exec(t))
									? ((B = [B, M.documentMode]),
									  (a = +a[1] + 4) != B[1] &&
											(I.push("IE " + B[1] + " mode"),
											N && (N[1] = ""),
											(B[1] = a)),
									  (B = "IE" == U ? String(B[1].toFixed(1)) : B[0]))
									: "number" == typeof M.documentMode &&
									  /^(?:Chrome|Firefox)\b/.test(U) &&
									  (I.push("masking as " + U + " " + B),
									  (U = "IE"),
									  (B = "11.0"),
									  (N = ["Trident"]),
									  (V = "Windows"));
							else if (
								(T &&
									((D = (a = T.lang.System).getProperty("os.arch")),
									(V =
										V ||
										a.getProperty("os.name") +
											" " +
											a.getProperty("os.version"))),
								C)
							) {
								try {
									(B = n.require("ringo/engine").version.join(".")),
										(U = "RingoJS");
								} catch (e) {
									(a = n.system) &&
										a.global.system == n.system &&
										((U = "Narwhal"), V || (V = a[0].os || null));
								}
								U || (U = "Rhino");
							} else
								"object" == typeof n.process &&
									!n.process.browser &&
									(a = n.process) &&
									("object" == typeof a.versions &&
										("string" == typeof a.versions.electron
											? (I.push("Node " + a.versions.node),
											  (U = "Electron"),
											  (B = a.versions.electron))
											: "string" == typeof a.versions.nw &&
											  (I.push("Chromium " + B, "Node " + a.versions.node),
											  (U = "NW.js"),
											  (B = a.versions.nw))),
									U ||
										((U = "Node.js"),
										(D = a.arch),
										(V = a.platform),
										(B = (B = /[\d.]+/.exec(a.version)) ? B[0] : null)));
							V = V && y(V);
						}
						if (
							(B &&
								(a =
									/(?:[ab]|dp|pre|[ab]\d+pre)(?:\d+\+?)?$/i.exec(B) ||
									/(?:alpha|beta)(?: ?\d)?/i.exec(
										t + ";" + (j && i.appMinorVersion)
									) ||
									(/\bMinefield\b/i.test(t) && "a")) &&
								((k = /b/i.test(a) ? "beta" : "alpha"),
								(B =
									B.replace(RegExp(a + "\\+?$"), "") +
									("beta" == k ? E : R) +
									(/\d+\+?/.exec(a) || ""))),
							"Fennec" == U ||
								("Firefox" == U && /\b(?:Android|Firefox OS|KaiOS)\b/.test(V)))
						)
							U = "Firefox Mobile";
						else if ("Maxthon" == U && B) B = B.replace(/\.[\d.]+/, ".x");
						else if (/\bXbox\b/i.test(_))
							"Xbox 360" == _ && (V = null),
								"Xbox 360" == _ &&
									/\bIEMobile\b/.test(t) &&
									I.unshift("mobile mode");
						else if (
							(!/^(?:Chrome|IE|Opera)$/.test(U) &&
								(!U || _ || /Browser|Mobi/.test(U))) ||
							("Windows CE" != V && !/Mobi/i.test(t))
						)
							if ("IE" == U && j)
								try {
									null === n.external && I.unshift("platform preview");
								} catch (e) {
									I.unshift("embedded");
								}
							else
								(/\bBlackBerry\b/.test(_) || /\bBB10\b/.test(t)) &&
								(a =
									(RegExp(_.replace(/ +/g, " *") + "/([.\\d]+)", "i").exec(t) ||
										0)[1] || B)
									? ((V =
											((a = [a, /BB10/.test(t)])[1]
												? ((_ = null), (q = "BlackBerry"))
												: "Device Software") +
											" " +
											a[0]),
									  (B = null))
									: this != m &&
									  "Wii" != _ &&
									  ((j && L) ||
											(/Opera/.test(U) && /\b(?:MSIE|Firefox)\b/i.test(t)) ||
											("Firefox" == U && /\bOS X (?:\d+\.){2,}/.test(V)) ||
											("IE" == U &&
												((V && !/^Win/.test(V) && B > 5.5) ||
													(/\bWindows XP\b/.test(V) && B > 8) ||
													(8 == B && !/\bTrident\b/.test(t))))) &&
									  !f.test((a = e.call(m, t.replace(f, "") + ";"))) &&
									  a.name &&
									  ((a =
											"ing as " + a.name + ((a = a.version) ? " " + a : "")),
									  f.test(U)
											? (/\bIE\b/.test(a) && "Mac OS" == V && (V = null),
											  (a = "identify" + a))
											: ((a = "mask" + a),
											  (U = x
													? y(x.replace(/([a-z])([A-Z])/g, "$1 $2"))
													: "Opera"),
											  /\bIE\b/.test(a) && (V = null),
											  j || (B = null)),
									  (N = ["Presto"]),
									  I.push(a));
						else U += " Mobile";
						(a = (/\bAppleWebKit\/([\d.]+\+?)/i.exec(t) || 0)[1]) &&
							((a = [parseFloat(a.replace(/\.(\d)$/, ".0$1")), a]),
							"Safari" == U && "+" == a[1].slice(-1)
								? ((U = "WebKit Nightly"),
								  (k = "alpha"),
								  (B = a[1].slice(0, -1)))
								: (B != a[1] &&
										B != (a[2] = (/\bSafari\/([\d.]+\+?)/i.exec(t) || 0)[1])) ||
								  (B = null),
							(a[1] = (/\b(?:Headless)?Chrome\/([\d.]+)/i.exec(t) || 0)[1]),
							537.36 == a[0] &&
								537.36 == a[2] &&
								parseFloat(a[1]) >= 28 &&
								"WebKit" == N &&
								(N = ["Blink"]),
							j && (h || a[1])
								? (N && (N[1] = "like Chrome"),
								  (a =
										a[1] ||
										((a = a[0]) < 530
											? 1
											: a < 532
											? 2
											: a < 532.05
											? 3
											: a < 533
											? 4
											: a < 534.03
											? 5
											: a < 534.07
											? 6
											: a < 534.1
											? 7
											: a < 534.13
											? 8
											: a < 534.16
											? 9
											: a < 534.24
											? 10
											: a < 534.3
											? 11
											: a < 535.01
											? 12
											: a < 535.02
											? "13+"
											: a < 535.07
											? 15
											: a < 535.11
											? 16
											: a < 535.19
											? 17
											: a < 536.05
											? 18
											: a < 536.1
											? 19
											: a < 537.01
											? 20
											: a < 537.11
											? "21+"
											: a < 537.13
											? 23
											: a < 537.18
											? 24
											: a < 537.24
											? 25
											: a < 537.36
											? 26
											: "Blink" != N
											? "27"
											: "28")))
								: (N && (N[1] = "like Safari"),
								  (a =
										(a = a[0]) < 400
											? 1
											: a < 500
											? 2
											: a < 526
											? 3
											: a < 533
											? 4
											: a < 534
											? "4+"
											: a < 535
											? 5
											: a < 537
											? 6
											: a < 538
											? 7
											: a < 601
											? 8
											: a < 602
											? 9
											: a < 604
											? 10
											: a < 606
											? 11
											: a < 608
											? 12
											: "12")),
							N &&
								(N[1] +=
									" " +
									(a +=
										"number" == typeof a ? ".x" : /[.+]/.test(a) ? "" : "+")),
							"Safari" == U && (!B || parseInt(B) > 45)
								? (B = a)
								: "Chrome" == U &&
								  /\bHeadlessChrome/i.test(t) &&
								  I.unshift("headless")),
							"Opera" == U && (a = /\bzbov|zvav$/.exec(V))
								? ((U += " "),
								  I.unshift("desktop mode"),
								  "zvav" == a ? ((U += "Mini"), (B = null)) : (U += "Mobile"),
								  (V = V.replace(RegExp(" *" + a + "$"), "")))
								: "Safari" == U && /\bChrome\b/.exec(N && N[1])
								? (I.unshift("desktop mode"),
								  (U = "Chrome Mobile"),
								  (B = null),
								  /\bOS X\b/.test(V)
										? ((q = "Apple"), (V = "iOS 4.3+"))
										: (V = null))
								: /\bSRWare Iron\b/.test(U) && !B && (B = z("Chrome")),
							B &&
								0 == B.indexOf((a = /[\d.]+$/.exec(V))) &&
								t.indexOf("/" + a + "-") > -1 &&
								(V = P(V.replace(a, ""))),
							V &&
								-1 != V.indexOf(U) &&
								!RegExp(U + " OS").test(V) &&
								(V = V.replace(RegExp(" *" + w(U) + " *"), "")),
							N &&
								!/\b(?:Avant|Nook)\b/.test(U) &&
								(/Browser|Lunascape|Maxthon/.test(U) ||
									("Safari" != U &&
										/^iOS/.test(V) &&
										/\bSafari\b/.test(N[1])) ||
									(/^(?:Adobe|Arora|Breach|Midori|Opera|Phantom|Rekonq|Rock|Samsung Internet|Sleipnir|SRWare Iron|Vivaldi|Web)/.test(
										U
									) &&
										N[1])) &&
								(a = N[N.length - 1]) &&
								I.push(a),
							I.length && (I = ["(" + I.join("; ") + ")"]),
							q && _ && _.indexOf(q) < 0 && I.push("on " + q),
							_ && I.push((/^on /.test(I[I.length - 1]) ? "" : "on ") + _),
							V &&
								((a = / ([\d.+]+)$/.exec(V)),
								(u = a && "/" == V.charAt(V.length - a[0].length - 1)),
								(V = {
									architecture: 32,
									family: a && !u ? V.replace(a[0], "") : V,
									version: a ? a[1] : null,
									toString: function () {
										var e = this.version;
										return (
											this.family +
											(e && !u ? " " + e : "") +
											(64 == this.architecture ? " 64-bit" : "")
										);
									},
								})),
							(a = /\b(?:AMD|IA|Win|WOW|x86_|x)64\b/i.exec(D)) &&
							!/\bi686\b/i.test(D)
								? (V &&
										((V.architecture = 64),
										(V.family = V.family.replace(RegExp(" *" + a), ""))),
								  U &&
										(/\bWOW64\b/i.test(t) ||
											(j &&
												/\w(?:86|32)$/.test(i.cpuClass || i.platform) &&
												!/\bWin64; x64\b/i.test(t))) &&
										I.unshift("32-bit"))
								: V &&
								  /^OS X/.test(V.family) &&
								  "Chrome" == U &&
								  parseFloat(B) >= 39 &&
								  (V.architecture = 64),
							t || (t = null);
						var W = {};
						return (
							(W.description = t),
							(W.layout = N && N[0]),
							(W.manufacturer = q),
							(W.name = U),
							(W.prerelease = k),
							(W.product = _),
							(W.ua = t),
							(W.version = U && B),
							(W.os = V || {
								architecture: null,
								family: null,
								version: null,
								toString: function () {
									return "null";
								},
							}),
							(W.parse = e),
							(W.toString = function () {
								return this.description || "";
							}),
							W.version && I.unshift(B),
							W.name && I.unshift(U),
							V &&
								U &&
								(V != String(V).split(" ")[0] ||
									(V != U.split(" ")[0] && !_)) &&
								I.push(_ ? "(" + V + ")" : "on " + V),
							I.length && (W.description = I.join(" ")),
							W
						);
					})();
					(s.platform = v),
						void 0 ===
							(i = function () {
								return v;
							}.call(t, n, t, e)) || (e.exports = i);
				}).call(this);
			}).call(this, n(24)(e), n(10));
		},
		function (e, t, n) {
			"use strict";
			(function (e) {
				var r;
				n.d(t, "c", function () {
					return o;
				}),
					n.d(t, "b", function () {
						return s;
					}),
					n.d(t, "d", function () {
						return a;
					}),
					n.d(t, "a", function () {
						return c;
					}),
					(function (e) {
						(e.INFO = "info"),
							(e.DEBUG = "debug"),
							(e.WARN = "warn"),
							(e.ERROR = "error");
					})(r || (r = {}));
				var i = function (e) {
						return (
							!(!window || void 0 === window.conflib || !window.conflib.log) &&
							(function (e) {
								switch (e) {
									case r.INFO:
										return window.conflib.log.info;
									case r.DEBUG:
										return window.conflib.log.debug;
									case r.ERROR:
										return window.conflib.log.error;
									case r.WARN:
									default:
										return window.conflib.log.warn;
								}
							})(e)
						);
					},
					o = function (e, t) {
						for (var n = [], o = 2; o < arguments.length; o++)
							n[o - 2] = arguments[o];
						i(r.INFO) && console.info("@" + e, t, n);
					},
					s = function (e, t) {
						for (var n = [], o = 2; o < arguments.length; o++)
							n[o - 2] = arguments[o];
						i(r.ERROR) && console.error("@" + e, t, n);
					},
					a = function (e, t) {
						for (var n = [], o = 2; o < arguments.length; o++)
							n[o - 2] = arguments[o];
						i(r.WARN) && console.warn("@" + e, t, n);
					},
					u = function (e, t) {
						for (var n = [], o = 2; o < arguments.length; o++)
							n[o - 2] = arguments[o];
						i(r.DEBUG) && console.debug("@" + e, t, n);
					};
				function c(e) {
					return {
						info: function (t) {
							for (var n = [], r = 1; r < arguments.length; r++)
								n[r - 1] = arguments[r];
							return o(e, t, n);
						},
						debug: function (t) {
							for (var n = [], r = 1; r < arguments.length; r++)
								n[r - 1] = arguments[r];
							return u(e, t, n);
						},
						warn: function (t) {
							for (var n = [], r = 1; r < arguments.length; r++)
								n[r - 1] = arguments[r];
							return a(e, t, n);
						},
						error: function (t) {
							for (var n = [], r = 1; r < arguments.length; r++)
								n[r - 1] = arguments[r];
							return s(e, t, n);
						},
					};
				}
			}).call(this, n(10));
		},
		,
		,
		function (e, t, n) {
			"use strict";
			(function (e) {
				var r = t;
				function i(e, t, n) {
					for (var r = Object.keys(t), i = 0; i < r.length; ++i)
						(void 0 !== e[r[i]] && n) || (e[r[i]] = t[r[i]]);
					return e;
				}
				function o(e) {
					function t(e, n) {
						if (!(this instanceof t)) return new t(e, n);
						Object.defineProperty(this, "message", {
							get: function () {
								return e;
							},
						}),
							Error.captureStackTrace
								? Error.captureStackTrace(this, t)
								: Object.defineProperty(this, "stack", {
										value: new Error().stack || "",
								  }),
							n && i(this, n);
					}
					return (
						((t.prototype = Object.create(Error.prototype)).constructor = t),
						Object.defineProperty(t.prototype, "name", {
							get: function () {
								return e;
							},
						}),
						(t.prototype.toString = function () {
							return this.name + ": " + this.message;
						}),
						t
					);
				}
				(r.asPromise = n(26)),
					(r.base64 = n(27)),
					(r.EventEmitter = n(28)),
					(r.float = n(29)),
					(r.inquire = n(30)),
					(r.utf8 = n(31)),
					(r.pool = n(32)),
					(r.LongBits = n(33)),
					(r.isNode = Boolean(
						void 0 !== e &&
							e &&
							e.process &&
							e.process.versions &&
							e.process.versions.node
					)),
					(r.global =
						(r.isNode && e) ||
						("undefined" != typeof window && window) ||
						("undefined" != typeof self && self) ||
						this),
					(r.emptyArray = Object.freeze ? Object.freeze([]) : []),
					(r.emptyObject = Object.freeze ? Object.freeze({}) : {}),
					(r.isInteger =
						Number.isInteger ||
						function (e) {
							return "number" == typeof e && isFinite(e) && Math.floor(e) === e;
						}),
					(r.isString = function (e) {
						return "string" == typeof e || e instanceof String;
					}),
					(r.isObject = function (e) {
						return e && "object" == typeof e;
					}),
					(r.isset = r.isSet =
						function (e, t) {
							var n = e[t];
							return (
								!(null == n || !e.hasOwnProperty(t)) &&
								("object" != typeof n ||
									(Array.isArray(n) ? n.length : Object.keys(n).length) > 0)
							);
						}),
					(r.Buffer = (function () {
						try {
							var e = r.inquire("buffer").Buffer;
							return e.prototype.utf8Write ? e : null;
						} catch (e) {
							return null;
						}
					})()),
					(r._Buffer_from = null),
					(r._Buffer_allocUnsafe = null),
					(r.newBuffer = function (e) {
						return "number" == typeof e
							? r.Buffer
								? r._Buffer_allocUnsafe(e)
								: new r.Array(e)
							: r.Buffer
							? r._Buffer_from(e)
							: "undefined" == typeof Uint8Array
							? e
							: new Uint8Array(e);
					}),
					(r.Array = "undefined" != typeof Uint8Array ? Uint8Array : Array),
					(r.Long =
						(r.global.dcodeIO && r.global.dcodeIO.Long) ||
						r.global.Long ||
						r.inquire("long")),
					(r.key2Re = /^true|false|0|1$/),
					(r.key32Re = /^-?(?:0|[1-9][0-9]*)$/),
					(r.key64Re = /^(?:[\\x00-\\xff]{8}|-?(?:0|[1-9][0-9]*))$/),
					(r.longToHash = function (e) {
						return e ? r.LongBits.from(e).toHash() : r.LongBits.zeroHash;
					}),
					(r.longFromHash = function (e, t) {
						var n = r.LongBits.fromHash(e);
						return r.Long
							? r.Long.fromBits(n.lo, n.hi, t)
							: n.toNumber(Boolean(t));
					}),
					(r.merge = i),
					(r.lcFirst = function (e) {
						return e.charAt(0).toLowerCase() + e.substring(1);
					}),
					(r.newError = o),
					(r.ProtocolError = o("ProtocolError")),
					(r.oneOfGetter = function (e) {
						for (var t = {}, n = 0; n < e.length; ++n) t[e[n]] = 1;
						return function () {
							for (var e = Object.keys(this), n = e.length - 1; n > -1; --n)
								if (
									1 === t[e[n]] &&
									void 0 !== this[e[n]] &&
									null !== this[e[n]]
								)
									return e[n];
						};
					}),
					(r.oneOfSetter = function (e) {
						return function (t) {
							for (var n = 0; n < e.length; ++n)
								e[n] !== t && delete this[e[n]];
						};
					}),
					(r.toJSONOptions = {
						longs: String,
						enums: String,
						bytes: String,
						json: !0,
					}),
					(r._configure = function () {
						var e = r.Buffer;
						e
							? ((r._Buffer_from =
									(e.from !== Uint8Array.from && e.from) ||
									function (t, n) {
										return new e(t, n);
									}),
							  (r._Buffer_allocUnsafe =
									e.allocUnsafe ||
									function (t) {
										return new e(t);
									}))
							: (r._Buffer_from = r._Buffer_allocUnsafe = null);
					});
			}).call(this, n(10));
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = n(45),
				i = n(49),
				o = n(50),
				s = n(51),
				a = n(13),
				u = (function () {
					function e(e) {
						(this._isScalar = !1), e && (this._subscribe = e);
					}
					return (
						(e.prototype.lift = function (t) {
							var n = new e();
							return (n.source = this), (n.operator = t), n;
						}),
						(e.prototype.subscribe = function (e, t, n) {
							var r = this.operator,
								o = i.toSubscriber(e, t, n);
							if (
								(r
									? o.add(r.call(o, this.source))
									: o.add(
											this.source ||
												(a.config.useDeprecatedSynchronousErrorHandling &&
													!o.syncErrorThrowable)
												? this._subscribe(o)
												: this._trySubscribe(o)
									  ),
								a.config.useDeprecatedSynchronousErrorHandling &&
									o.syncErrorThrowable &&
									((o.syncErrorThrowable = !1), o.syncErrorThrown))
							)
								throw o.syncErrorValue;
							return o;
						}),
						(e.prototype._trySubscribe = function (e) {
							try {
								return this._subscribe(e);
							} catch (t) {
								a.config.useDeprecatedSynchronousErrorHandling &&
									((e.syncErrorThrown = !0), (e.syncErrorValue = t)),
									r.canReportError(e) ? e.error(t) : console.warn(t);
							}
						}),
						(e.prototype.forEach = function (e, t) {
							var n = this;
							return new (t = c(t))(function (t, r) {
								var i;
								i = n.subscribe(
									function (t) {
										try {
											e(t);
										} catch (e) {
											r(e), i && i.unsubscribe();
										}
									},
									r,
									t
								);
							});
						}),
						(e.prototype._subscribe = function (e) {
							var t = this.source;
							return t && t.subscribe(e);
						}),
						(e.prototype[o.observable] = function () {
							return this;
						}),
						(e.prototype.pipe = function () {
							for (var e = [], t = 0; t < arguments.length; t++)
								e[t] = arguments[t];
							return 0 === e.length ? this : s.pipeFromArray(e)(this);
						}),
						(e.prototype.toPromise = function (e) {
							var t = this;
							return new (e = c(e))(function (e, n) {
								var r;
								t.subscribe(
									function (e) {
										return (r = e);
									},
									function (e) {
										return n(e);
									},
									function () {
										return e(r);
									}
								);
							});
						}),
						(e.create = function (t) {
							return new e(t);
						}),
						e
					);
				})();
			function c(e) {
				if ((e || (e = a.config.Promise || Promise), !e))
					throw new Error("no Promise impl found");
				return e;
			}
			t.Observable = u;
		},
		function (e) {
			e.exports = JSON.parse('{"a":"1.5.46-web.prod.build5"}');
		},
		function (e, t) {
			var n;
			n = (function () {
				return this;
			})();
			try {
				n = n || new Function("return this")();
			} catch (e) {
				"object" == typeof window && (n = window);
			}
			e.exports = n;
		},
		function (module, exports, __webpack_require__) {
			var e;
			window,
				(e = function () {
					return (function (e) {
						var t = {};
						function n(r) {
							if (t[r]) return t[r].exports;
							var i = (t[r] = { i: r, l: !1, exports: {} });
							return (
								e[r].call(i.exports, i, i.exports, n), (i.l = !0), i.exports
							);
						}
						return (
							(n.m = e),
							(n.c = t),
							(n.d = function (e, t, r) {
								n.o(e, t) ||
									Object.defineProperty(e, t, { enumerable: !0, get: r });
							}),
							(n.r = function (e) {
								"undefined" != typeof Symbol &&
									Symbol.toStringTag &&
									Object.defineProperty(e, Symbol.toStringTag, {
										value: "Module",
									}),
									Object.defineProperty(e, "__esModule", { value: !0 });
							}),
							(n.t = function (e, t) {
								if ((1 & t && (e = n(e)), 8 & t)) return e;
								if (4 & t && "object" == typeof e && e && e.__esModule)
									return e;
								var r = Object.create(null);
								if (
									(n.r(r),
									Object.defineProperty(r, "default", {
										enumerable: !0,
										value: e,
									}),
									2 & t && "string" != typeof e)
								)
									for (var i in e)
										n.d(
											r,
											i,
											function (t) {
												return e[t];
											}.bind(null, i)
										);
								return r;
							}),
							(n.n = function (e) {
								var t =
									e && e.__esModule
										? function () {
												return e.default;
										  }
										: function () {
												return e;
										  };
								return n.d(t, "a", t), t;
							}),
							(n.o = function (e, t) {
								return Object.prototype.hasOwnProperty.call(e, t);
							}),
							(n.p = ""),
							n((n.s = 15))
						);
					})([
						function (e, t, n) {
							"use strict";
							var r = n(6),
								i = Object.prototype.toString;
							function o(e) {
								return "[object Array]" === i.call(e);
							}
							function s(e) {
								return void 0 === e;
							}
							function a(e) {
								return null !== e && "object" == typeof e;
							}
							function u(e) {
								if ("[object Object]" !== i.call(e)) return !1;
								var t = Object.getPrototypeOf(e);
								return null === t || t === Object.prototype;
							}
							function c(e) {
								return "[object Function]" === i.call(e);
							}
							function l(e, t) {
								if (null != e)
									if (("object" != typeof e && (e = [e]), o(e)))
										for (var n = 0, r = e.length; n < r; n++)
											t.call(null, e[n], n, e);
									else
										for (var i in e)
											Object.prototype.hasOwnProperty.call(e, i) &&
												t.call(null, e[i], i, e);
							}
							e.exports = {
								isArray: o,
								isArrayBuffer: function (e) {
									return "[object ArrayBuffer]" === i.call(e);
								},
								isBuffer: function (e) {
									return (
										null !== e &&
										!s(e) &&
										null !== e.constructor &&
										!s(e.constructor) &&
										"function" == typeof e.constructor.isBuffer &&
										e.constructor.isBuffer(e)
									);
								},
								isFormData: function (e) {
									return (
										"undefined" != typeof FormData && e instanceof FormData
									);
								},
								isArrayBufferView: function (e) {
									return "undefined" != typeof ArrayBuffer && ArrayBuffer.isView
										? ArrayBuffer.isView(e)
										: e && e.buffer && e.buffer instanceof ArrayBuffer;
								},
								isString: function (e) {
									return "string" == typeof e;
								},
								isNumber: function (e) {
									return "number" == typeof e;
								},
								isObject: a,
								isPlainObject: u,
								isUndefined: s,
								isDate: function (e) {
									return "[object Date]" === i.call(e);
								},
								isFile: function (e) {
									return "[object File]" === i.call(e);
								},
								isBlob: function (e) {
									return "[object Blob]" === i.call(e);
								},
								isFunction: c,
								isStream: function (e) {
									return a(e) && c(e.pipe);
								},
								isURLSearchParams: function (e) {
									return (
										"undefined" != typeof URLSearchParams &&
										e instanceof URLSearchParams
									);
								},
								isStandardBrowserEnv: function () {
									return (
										("undefined" == typeof navigator ||
											("ReactNative" !== navigator.product &&
												"NativeScript" !== navigator.product &&
												"NS" !== navigator.product)) &&
										"undefined" != typeof window &&
										"undefined" != typeof document
									);
								},
								forEach: l,
								merge: function e() {
									var t = {};
									function n(n, r) {
										u(t[r]) && u(n)
											? (t[r] = e(t[r], n))
											: u(n)
											? (t[r] = e({}, n))
											: o(n)
											? (t[r] = n.slice())
											: (t[r] = n);
									}
									for (var r = 0, i = arguments.length; r < i; r++)
										l(arguments[r], n);
									return t;
								},
								extend: function (e, t, n) {
									return (
										l(t, function (t, i) {
											e[i] = n && "function" == typeof t ? r(t, n) : t;
										}),
										e
									);
								},
								trim: function (e) {
									return e.replace(/^\s*/, "").replace(/\s*$/, "");
								},
								stripBOM: function (e) {
									return 65279 === e.charCodeAt(0) && (e = e.slice(1)), e;
								},
							};
						},
						function (e, t, n) {
							"use strict";
							(function (e) {
								var r = t;
								function i(e, t, n) {
									for (var r = Object.keys(t), i = 0; i < r.length; ++i)
										(void 0 !== e[r[i]] && n) || (e[r[i]] = t[r[i]]);
									return e;
								}
								function o(e) {
									function t(e, n) {
										if (!(this instanceof t)) return new t(e, n);
										Object.defineProperty(this, "message", {
											get: function () {
												return e;
											},
										}),
											Error.captureStackTrace
												? Error.captureStackTrace(this, t)
												: Object.defineProperty(this, "stack", {
														value: new Error().stack || "",
												  }),
											n && i(this, n);
									}
									return (
										((t.prototype = Object.create(
											Error.prototype
										)).constructor = t),
										Object.defineProperty(t.prototype, "name", {
											get: function () {
												return e;
											},
										}),
										(t.prototype.toString = function () {
											return this.name + ": " + this.message;
										}),
										t
									);
								}
								(r.asPromise = n(19)),
									(r.base64 = n(20)),
									(r.EventEmitter = n(21)),
									(r.float = n(22)),
									(r.inquire = n(23)),
									(r.utf8 = n(24)),
									(r.pool = n(25)),
									(r.LongBits = n(26)),
									(r.isNode = Boolean(
										void 0 !== e &&
											e &&
											e.process &&
											e.process.versions &&
											e.process.versions.node
									)),
									(r.global =
										(r.isNode && e) ||
										("undefined" != typeof window && window) ||
										("undefined" != typeof self && self) ||
										this),
									(r.emptyArray = Object.freeze ? Object.freeze([]) : []),
									(r.emptyObject = Object.freeze ? Object.freeze({}) : {}),
									(r.isInteger =
										Number.isInteger ||
										function (e) {
											return (
												"number" == typeof e &&
												isFinite(e) &&
												Math.floor(e) === e
											);
										}),
									(r.isString = function (e) {
										return "string" == typeof e || e instanceof String;
									}),
									(r.isObject = function (e) {
										return e && "object" == typeof e;
									}),
									(r.isset = r.isSet =
										function (e, t) {
											var n = e[t];
											return (
												!(null == n || !e.hasOwnProperty(t)) &&
												("object" != typeof n ||
													(Array.isArray(n)
														? n.length
														: Object.keys(n).length) > 0)
											);
										}),
									(r.Buffer = (function () {
										try {
											var e = r.inquire("buffer").Buffer;
											return e.prototype.utf8Write ? e : null;
										} catch (e) {
											return null;
										}
									})()),
									(r._Buffer_from = null),
									(r._Buffer_allocUnsafe = null),
									(r.newBuffer = function (e) {
										return "number" == typeof e
											? r.Buffer
												? r._Buffer_allocUnsafe(e)
												: new r.Array(e)
											: r.Buffer
											? r._Buffer_from(e)
											: "undefined" == typeof Uint8Array
											? e
											: new Uint8Array(e);
									}),
									(r.Array =
										"undefined" != typeof Uint8Array ? Uint8Array : Array),
									(r.Long =
										(r.global.dcodeIO && r.global.dcodeIO.Long) ||
										r.global.Long ||
										r.inquire("long")),
									(r.key2Re = /^true|false|0|1$/),
									(r.key32Re = /^-?(?:0|[1-9][0-9]*)$/),
									(r.key64Re = /^(?:[\\x00-\\xff]{8}|-?(?:0|[1-9][0-9]*))$/),
									(r.longToHash = function (e) {
										return e
											? r.LongBits.from(e).toHash()
											: r.LongBits.zeroHash;
									}),
									(r.longFromHash = function (e, t) {
										var n = r.LongBits.fromHash(e);
										return r.Long
											? r.Long.fromBits(n.lo, n.hi, t)
											: n.toNumber(Boolean(t));
									}),
									(r.merge = i),
									(r.lcFirst = function (e) {
										return e.charAt(0).toLowerCase() + e.substring(1);
									}),
									(r.newError = o),
									(r.ProtocolError = o("ProtocolError")),
									(r.oneOfGetter = function (e) {
										for (var t = {}, n = 0; n < e.length; ++n) t[e[n]] = 1;
										return function () {
											for (
												var e = Object.keys(this), n = e.length - 1;
												n > -1;
												--n
											)
												if (
													1 === t[e[n]] &&
													void 0 !== this[e[n]] &&
													null !== this[e[n]]
												)
													return e[n];
										};
									}),
									(r.oneOfSetter = function (e) {
										return function (t) {
											for (var n = 0; n < e.length; ++n)
												e[n] !== t && delete this[e[n]];
										};
									}),
									(r.toJSONOptions = {
										longs: String,
										enums: String,
										bytes: String,
										json: !0,
									}),
									(r._configure = function () {
										var e = r.Buffer;
										e
											? ((r._Buffer_from =
													(e.from !== Uint8Array.from && e.from) ||
													function (t, n) {
														return new e(t, n);
													}),
											  (r._Buffer_allocUnsafe =
													e.allocUnsafe ||
													function (t) {
														return new e(t);
													}))
											: (r._Buffer_from = r._Buffer_allocUnsafe = null);
									});
							}).call(this, n(18));
						},
						function (e, t, n) {
							"use strict";
							var r = n(16),
								i = r.Reader,
								o = r.Writer,
								s = r.util,
								a = r.roots.default || (r.roots.default = {});
							(a.AgentInfo = (function () {
								function e(e) {
									if (e)
										for (var t = Object.keys(e), n = 0; n < t.length; ++n)
											null != e[t[n]] && (this[t[n]] = e[t[n]]);
								}
								return (
									(e.prototype.pid = ""),
									(e.prototype.origin = ""),
									(e.prototype.contentId = ""),
									(e.prototype.apiKey = ""),
									(e.prototype.version = ""),
									(e.prototype.jsonFileds = ""),
									(e.prototype.ip = ""),
									(e.prototype.userId = ""),
									(e.prototype.isp = ""),
									(e.prototype.userAgent = ""),
									(e.create = function (t) {
										return new e(t);
									}),
									(e.encode = function (e, t) {
										return (
											t || (t = o.create()),
											null != e.pid &&
												Object.hasOwnProperty.call(e, "pid") &&
												t.uint32(10).string(e.pid),
											null != e.origin &&
												Object.hasOwnProperty.call(e, "origin") &&
												t.uint32(18).string(e.origin),
											null != e.contentId &&
												Object.hasOwnProperty.call(e, "contentId") &&
												t.uint32(26).string(e.contentId),
											null != e.apiKey &&
												Object.hasOwnProperty.call(e, "apiKey") &&
												t.uint32(34).string(e.apiKey),
											null != e.version &&
												Object.hasOwnProperty.call(e, "version") &&
												t.uint32(50).string(e.version),
											null != e.jsonFileds &&
												Object.hasOwnProperty.call(e, "jsonFileds") &&
												t.uint32(82).string(e.jsonFileds),
											null != e.ip &&
												Object.hasOwnProperty.call(e, "ip") &&
												t.uint32(90).string(e.ip),
											null != e.userId &&
												Object.hasOwnProperty.call(e, "userId") &&
												t.uint32(98).string(e.userId),
											null != e.isp &&
												Object.hasOwnProperty.call(e, "isp") &&
												t.uint32(106).string(e.isp),
											null != e.userAgent &&
												Object.hasOwnProperty.call(e, "userAgent") &&
												t.uint32(114).string(e.userAgent),
											t
										);
									}),
									(e.encodeDelimited = function (e, t) {
										return this.encode(e, t).ldelim();
									}),
									(e.decode = function (e, t) {
										e instanceof i || (e = i.create(e));
										for (
											var n = void 0 === t ? e.len : e.pos + t,
												r = new a.AgentInfo();
											e.pos < n;

										) {
											var o = e.uint32();
											switch (o >>> 3) {
												case 1:
													r.pid = e.string();
													break;
												case 2:
													r.origin = e.string();
													break;
												case 3:
													r.contentId = e.string();
													break;
												case 4:
													r.apiKey = e.string();
													break;
												case 6:
													r.version = e.string();
													break;
												case 10:
													r.jsonFileds = e.string();
													break;
												case 11:
													r.ip = e.string();
													break;
												case 12:
													r.userId = e.string();
													break;
												case 13:
													r.isp = e.string();
													break;
												case 14:
													r.userAgent = e.string();
													break;
												default:
													e.skipType(7 & o);
											}
										}
										return r;
									}),
									(e.decodeDelimited = function (e) {
										return (
											e instanceof i || (e = new i(e)),
											this.decode(e, e.uint32())
										);
									}),
									(e.verify = function (e) {
										return "object" != typeof e || null === e
											? "object expected"
											: null != e.pid &&
											  e.hasOwnProperty("pid") &&
											  !s.isString(e.pid)
											? "pid: string expected"
											: null != e.origin &&
											  e.hasOwnProperty("origin") &&
											  !s.isString(e.origin)
											? "origin: string expected"
											: null != e.contentId &&
											  e.hasOwnProperty("contentId") &&
											  !s.isString(e.contentId)
											? "contentId: string expected"
											: null != e.apiKey &&
											  e.hasOwnProperty("apiKey") &&
											  !s.isString(e.apiKey)
											? "apiKey: string expected"
											: null != e.version &&
											  e.hasOwnProperty("version") &&
											  !s.isString(e.version)
											? "version: string expected"
											: null != e.jsonFileds &&
											  e.hasOwnProperty("jsonFileds") &&
											  !s.isString(e.jsonFileds)
											? "jsonFileds: string expected"
											: null != e.ip &&
											  e.hasOwnProperty("ip") &&
											  !s.isString(e.ip)
											? "ip: string expected"
											: null != e.userId &&
											  e.hasOwnProperty("userId") &&
											  !s.isString(e.userId)
											? "userId: string expected"
											: null != e.isp &&
											  e.hasOwnProperty("isp") &&
											  !s.isString(e.isp)
											? "isp: string expected"
											: null != e.userAgent &&
											  e.hasOwnProperty("userAgent") &&
											  !s.isString(e.userAgent)
											? "userAgent: string expected"
											: null;
									}),
									(e.fromObject = function (e) {
										if (e instanceof a.AgentInfo) return e;
										var t = new a.AgentInfo();
										return (
											null != e.pid && (t.pid = String(e.pid)),
											null != e.origin && (t.origin = String(e.origin)),
											null != e.contentId &&
												(t.contentId = String(e.contentId)),
											null != e.apiKey && (t.apiKey = String(e.apiKey)),
											null != e.version && (t.version = String(e.version)),
											null != e.jsonFileds &&
												(t.jsonFileds = String(e.jsonFileds)),
											null != e.ip && (t.ip = String(e.ip)),
											null != e.userId && (t.userId = String(e.userId)),
											null != e.isp && (t.isp = String(e.isp)),
											null != e.userAgent &&
												(t.userAgent = String(e.userAgent)),
											t
										);
									}),
									(e.toObject = function (e, t) {
										t || (t = {});
										var n = {};
										return (
											t.defaults &&
												((n.pid = ""),
												(n.origin = ""),
												(n.contentId = ""),
												(n.apiKey = ""),
												(n.version = ""),
												(n.jsonFileds = ""),
												(n.ip = ""),
												(n.userId = ""),
												(n.isp = ""),
												(n.userAgent = "")),
											null != e.pid &&
												e.hasOwnProperty("pid") &&
												(n.pid = e.pid),
											null != e.origin &&
												e.hasOwnProperty("origin") &&
												(n.origin = e.origin),
											null != e.contentId &&
												e.hasOwnProperty("contentId") &&
												(n.contentId = e.contentId),
											null != e.apiKey &&
												e.hasOwnProperty("apiKey") &&
												(n.apiKey = e.apiKey),
											null != e.version &&
												e.hasOwnProperty("version") &&
												(n.version = e.version),
											null != e.jsonFileds &&
												e.hasOwnProperty("jsonFileds") &&
												(n.jsonFileds = e.jsonFileds),
											null != e.ip && e.hasOwnProperty("ip") && (n.ip = e.ip),
											null != e.userId &&
												e.hasOwnProperty("userId") &&
												(n.userId = e.userId),
											null != e.isp &&
												e.hasOwnProperty("isp") &&
												(n.isp = e.isp),
											null != e.userAgent &&
												e.hasOwnProperty("userAgent") &&
												(n.userAgent = e.userAgent),
											n
										);
									}),
									(e.prototype.toJSON = function () {
										return this.constructor.toObject(
											this,
											r.util.toJSONOptions
										);
									}),
									e
								);
							})()),
								(a.MediaMetadata = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.videoFormat = ""),
										(e.prototype.vod = !1),
										(e.prototype.url = ""),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.videoFormat &&
													Object.hasOwnProperty.call(e, "videoFormat") &&
													t.uint32(10).string(e.videoFormat),
												null != e.vod &&
													Object.hasOwnProperty.call(e, "vod") &&
													t.uint32(24).bool(e.vod),
												null != e.url &&
													Object.hasOwnProperty.call(e, "url") &&
													t.uint32(34).string(e.url),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.MediaMetadata();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.videoFormat = e.string();
														break;
													case 3:
														r.vod = e.bool();
														break;
													case 4:
														r.url = e.string();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.videoFormat &&
												  e.hasOwnProperty("videoFormat") &&
												  !s.isString(e.videoFormat)
												? "videoFormat: string expected"
												: null != e.vod &&
												  e.hasOwnProperty("vod") &&
												  "boolean" != typeof e.vod
												? "vod: boolean expected"
												: null != e.url &&
												  e.hasOwnProperty("url") &&
												  !s.isString(e.url)
												? "url: string expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.MediaMetadata) return e;
											var t = new a.MediaMetadata();
											return (
												null != e.videoFormat &&
													(t.videoFormat = String(e.videoFormat)),
												null != e.vod && (t.vod = Boolean(e.vod)),
												null != e.url && (t.url = String(e.url)),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											return (
												t.defaults &&
													((n.videoFormat = ""), (n.vod = !1), (n.url = "")),
												null != e.videoFormat &&
													e.hasOwnProperty("videoFormat") &&
													(n.videoFormat = e.videoFormat),
												null != e.vod &&
													e.hasOwnProperty("vod") &&
													(n.vod = e.vod),
												null != e.url &&
													e.hasOwnProperty("url") &&
													(n.url = e.url),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.PeerMetrics = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.remotePid = ""),
										(e.prototype.timespent = 0),
										(e.prototype.sizeBytes = 0),
										(e.prototype.avgDelay = 0),
										(e.prototype.cntChunks = 0),
										(e.prototype.cntHasChunks = 0),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.remotePid &&
													Object.hasOwnProperty.call(e, "remotePid") &&
													t.uint32(10).string(e.remotePid),
												null != e.timespent &&
													Object.hasOwnProperty.call(e, "timespent") &&
													t.uint32(16).uint32(e.timespent),
												null != e.sizeBytes &&
													Object.hasOwnProperty.call(e, "sizeBytes") &&
													t.uint32(24).uint32(e.sizeBytes),
												null != e.avgDelay &&
													Object.hasOwnProperty.call(e, "avgDelay") &&
													t.uint32(32).uint32(e.avgDelay),
												null != e.cntChunks &&
													Object.hasOwnProperty.call(e, "cntChunks") &&
													t.uint32(40).uint32(e.cntChunks),
												null != e.cntHasChunks &&
													Object.hasOwnProperty.call(e, "cntHasChunks") &&
													t.uint32(80).uint32(e.cntHasChunks),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.PeerMetrics();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.remotePid = e.string();
														break;
													case 2:
														r.timespent = e.uint32();
														break;
													case 3:
														r.sizeBytes = e.uint32();
														break;
													case 4:
														r.avgDelay = e.uint32();
														break;
													case 5:
														r.cntChunks = e.uint32();
														break;
													case 10:
														r.cntHasChunks = e.uint32();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.remotePid &&
												  e.hasOwnProperty("remotePid") &&
												  !s.isString(e.remotePid)
												? "remotePid: string expected"
												: null != e.timespent &&
												  e.hasOwnProperty("timespent") &&
												  !s.isInteger(e.timespent)
												? "timespent: integer expected"
												: null != e.sizeBytes &&
												  e.hasOwnProperty("sizeBytes") &&
												  !s.isInteger(e.sizeBytes)
												? "sizeBytes: integer expected"
												: null != e.avgDelay &&
												  e.hasOwnProperty("avgDelay") &&
												  !s.isInteger(e.avgDelay)
												? "avgDelay: integer expected"
												: null != e.cntChunks &&
												  e.hasOwnProperty("cntChunks") &&
												  !s.isInteger(e.cntChunks)
												? "cntChunks: integer expected"
												: null != e.cntHasChunks &&
												  e.hasOwnProperty("cntHasChunks") &&
												  !s.isInteger(e.cntHasChunks)
												? "cntHasChunks: integer expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.PeerMetrics) return e;
											var t = new a.PeerMetrics();
											return (
												null != e.remotePid &&
													(t.remotePid = String(e.remotePid)),
												null != e.timespent &&
													(t.timespent = e.timespent >>> 0),
												null != e.sizeBytes &&
													(t.sizeBytes = e.sizeBytes >>> 0),
												null != e.avgDelay && (t.avgDelay = e.avgDelay >>> 0),
												null != e.cntChunks &&
													(t.cntChunks = e.cntChunks >>> 0),
												null != e.cntHasChunks &&
													(t.cntHasChunks = e.cntHasChunks >>> 0),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											return (
												t.defaults &&
													((n.remotePid = ""),
													(n.timespent = 0),
													(n.sizeBytes = 0),
													(n.avgDelay = 0),
													(n.cntChunks = 0),
													(n.cntHasChunks = 0)),
												null != e.remotePid &&
													e.hasOwnProperty("remotePid") &&
													(n.remotePid = e.remotePid),
												null != e.timespent &&
													e.hasOwnProperty("timespent") &&
													(n.timespent = e.timespent),
												null != e.sizeBytes &&
													e.hasOwnProperty("sizeBytes") &&
													(n.sizeBytes = e.sizeBytes),
												null != e.avgDelay &&
													e.hasOwnProperty("avgDelay") &&
													(n.avgDelay = e.avgDelay),
												null != e.cntChunks &&
													e.hasOwnProperty("cntChunks") &&
													(n.cntChunks = e.cntChunks),
												null != e.cntHasChunks &&
													e.hasOwnProperty("cntHasChunks") &&
													(n.cntHasChunks = e.cntHasChunks),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.PeerDelay = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.remotePid = ""),
										(e.prototype.avgDelay = 0),
										(e.prototype.cntPpmsg = 0),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.remotePid &&
													Object.hasOwnProperty.call(e, "remotePid") &&
													t.uint32(10).string(e.remotePid),
												null != e.avgDelay &&
													Object.hasOwnProperty.call(e, "avgDelay") &&
													t.uint32(16).uint32(e.avgDelay),
												null != e.cntPpmsg &&
													Object.hasOwnProperty.call(e, "cntPpmsg") &&
													t.uint32(24).uint32(e.cntPpmsg),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.PeerDelay();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.remotePid = e.string();
														break;
													case 2:
														r.avgDelay = e.uint32();
														break;
													case 3:
														r.cntPpmsg = e.uint32();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.remotePid &&
												  e.hasOwnProperty("remotePid") &&
												  !s.isString(e.remotePid)
												? "remotePid: string expected"
												: null != e.avgDelay &&
												  e.hasOwnProperty("avgDelay") &&
												  !s.isInteger(e.avgDelay)
												? "avgDelay: integer expected"
												: null != e.cntPpmsg &&
												  e.hasOwnProperty("cntPpmsg") &&
												  !s.isInteger(e.cntPpmsg)
												? "cntPpmsg: integer expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.PeerDelay) return e;
											var t = new a.PeerDelay();
											return (
												null != e.remotePid &&
													(t.remotePid = String(e.remotePid)),
												null != e.avgDelay && (t.avgDelay = e.avgDelay >>> 0),
												null != e.cntPpmsg && (t.cntPpmsg = e.cntPpmsg >>> 0),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											return (
												t.defaults &&
													((n.remotePid = ""),
													(n.avgDelay = 0),
													(n.cntPpmsg = 0)),
												null != e.remotePid &&
													e.hasOwnProperty("remotePid") &&
													(n.remotePid = e.remotePid),
												null != e.avgDelay &&
													e.hasOwnProperty("avgDelay") &&
													(n.avgDelay = e.avgDelay),
												null != e.cntPpmsg &&
													e.hasOwnProperty("cntPpmsg") &&
													(n.cntPpmsg = e.cntPpmsg),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.PlayerStats = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.cntPlay = 0),
										(e.prototype.cntPause = 0),
										(e.prototype.cntPrev = 0),
										(e.prototype.cntNext = 0),
										(e.prototype.cntMqc = 0),
										(e.prototype.cntFs = 0),
										(e.prototype.cntPip = 0),
										(e.prototype.cntSeek = 0),
										(e.prototype.cntLc = 0),
										(e.prototype.cntSc = 0),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.cntPlay &&
													Object.hasOwnProperty.call(e, "cntPlay") &&
													t.uint32(8).uint32(e.cntPlay),
												null != e.cntPause &&
													Object.hasOwnProperty.call(e, "cntPause") &&
													t.uint32(16).uint32(e.cntPause),
												null != e.cntPrev &&
													Object.hasOwnProperty.call(e, "cntPrev") &&
													t.uint32(24).uint32(e.cntPrev),
												null != e.cntNext &&
													Object.hasOwnProperty.call(e, "cntNext") &&
													t.uint32(32).uint32(e.cntNext),
												null != e.cntMqc &&
													Object.hasOwnProperty.call(e, "cntMqc") &&
													t.uint32(40).uint32(e.cntMqc),
												null != e.cntFs &&
													Object.hasOwnProperty.call(e, "cntFs") &&
													t.uint32(48).uint32(e.cntFs),
												null != e.cntPip &&
													Object.hasOwnProperty.call(e, "cntPip") &&
													t.uint32(56).uint32(e.cntPip),
												null != e.cntSeek &&
													Object.hasOwnProperty.call(e, "cntSeek") &&
													t.uint32(64).uint32(e.cntSeek),
												null != e.cntLc &&
													Object.hasOwnProperty.call(e, "cntLc") &&
													t.uint32(72).uint32(e.cntLc),
												null != e.cntSc &&
													Object.hasOwnProperty.call(e, "cntSc") &&
													t.uint32(80).uint32(e.cntSc),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.PlayerStats();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.cntPlay = e.uint32();
														break;
													case 2:
														r.cntPause = e.uint32();
														break;
													case 3:
														r.cntPrev = e.uint32();
														break;
													case 4:
														r.cntNext = e.uint32();
														break;
													case 5:
														r.cntMqc = e.uint32();
														break;
													case 6:
														r.cntFs = e.uint32();
														break;
													case 7:
														r.cntPip = e.uint32();
														break;
													case 8:
														r.cntSeek = e.uint32();
														break;
													case 9:
														r.cntLc = e.uint32();
														break;
													case 10:
														r.cntSc = e.uint32();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.cntPlay &&
												  e.hasOwnProperty("cntPlay") &&
												  !s.isInteger(e.cntPlay)
												? "cntPlay: integer expected"
												: null != e.cntPause &&
												  e.hasOwnProperty("cntPause") &&
												  !s.isInteger(e.cntPause)
												? "cntPause: integer expected"
												: null != e.cntPrev &&
												  e.hasOwnProperty("cntPrev") &&
												  !s.isInteger(e.cntPrev)
												? "cntPrev: integer expected"
												: null != e.cntNext &&
												  e.hasOwnProperty("cntNext") &&
												  !s.isInteger(e.cntNext)
												? "cntNext: integer expected"
												: null != e.cntMqc &&
												  e.hasOwnProperty("cntMqc") &&
												  !s.isInteger(e.cntMqc)
												? "cntMqc: integer expected"
												: null != e.cntFs &&
												  e.hasOwnProperty("cntFs") &&
												  !s.isInteger(e.cntFs)
												? "cntFs: integer expected"
												: null != e.cntPip &&
												  e.hasOwnProperty("cntPip") &&
												  !s.isInteger(e.cntPip)
												? "cntPip: integer expected"
												: null != e.cntSeek &&
												  e.hasOwnProperty("cntSeek") &&
												  !s.isInteger(e.cntSeek)
												? "cntSeek: integer expected"
												: null != e.cntLc &&
												  e.hasOwnProperty("cntLc") &&
												  !s.isInteger(e.cntLc)
												? "cntLc: integer expected"
												: null != e.cntSc &&
												  e.hasOwnProperty("cntSc") &&
												  !s.isInteger(e.cntSc)
												? "cntSc: integer expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.PlayerStats) return e;
											var t = new a.PlayerStats();
											return (
												null != e.cntPlay && (t.cntPlay = e.cntPlay >>> 0),
												null != e.cntPause && (t.cntPause = e.cntPause >>> 0),
												null != e.cntPrev && (t.cntPrev = e.cntPrev >>> 0),
												null != e.cntNext && (t.cntNext = e.cntNext >>> 0),
												null != e.cntMqc && (t.cntMqc = e.cntMqc >>> 0),
												null != e.cntFs && (t.cntFs = e.cntFs >>> 0),
												null != e.cntPip && (t.cntPip = e.cntPip >>> 0),
												null != e.cntSeek && (t.cntSeek = e.cntSeek >>> 0),
												null != e.cntLc && (t.cntLc = e.cntLc >>> 0),
												null != e.cntSc && (t.cntSc = e.cntSc >>> 0),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											return (
												t.defaults &&
													((n.cntPlay = 0),
													(n.cntPause = 0),
													(n.cntPrev = 0),
													(n.cntNext = 0),
													(n.cntMqc = 0),
													(n.cntFs = 0),
													(n.cntPip = 0),
													(n.cntSeek = 0),
													(n.cntLc = 0),
													(n.cntSc = 0)),
												null != e.cntPlay &&
													e.hasOwnProperty("cntPlay") &&
													(n.cntPlay = e.cntPlay),
												null != e.cntPause &&
													e.hasOwnProperty("cntPause") &&
													(n.cntPause = e.cntPause),
												null != e.cntPrev &&
													e.hasOwnProperty("cntPrev") &&
													(n.cntPrev = e.cntPrev),
												null != e.cntNext &&
													e.hasOwnProperty("cntNext") &&
													(n.cntNext = e.cntNext),
												null != e.cntMqc &&
													e.hasOwnProperty("cntMqc") &&
													(n.cntMqc = e.cntMqc),
												null != e.cntFs &&
													e.hasOwnProperty("cntFs") &&
													(n.cntFs = e.cntFs),
												null != e.cntPip &&
													e.hasOwnProperty("cntPip") &&
													(n.cntPip = e.cntPip),
												null != e.cntSeek &&
													e.hasOwnProperty("cntSeek") &&
													(n.cntSeek = e.cntSeek),
												null != e.cntLc &&
													e.hasOwnProperty("cntLc") &&
													(n.cntLc = e.cntLc),
												null != e.cntSc &&
													e.hasOwnProperty("cntSc") &&
													(n.cntSc = e.cntSc),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.DataStats = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.bytesCdn = 0),
										(e.prototype.bytesP2p = 0),
										(e.prototype.bytesP2pUpload = 0),
										(e.prototype.timespentCdn = 0),
										(e.prototype.timespentP2p = 0),
										(e.prototype.timespentP2pUpload = 0),
										(e.prototype.cntCdn = 0),
										(e.prototype.cntP2p = 0),
										(e.prototype.cntP2pUpload = 0),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.bytesCdn &&
													Object.hasOwnProperty.call(e, "bytesCdn") &&
													t.uint32(8).uint32(e.bytesCdn),
												null != e.bytesP2p &&
													Object.hasOwnProperty.call(e, "bytesP2p") &&
													t.uint32(16).uint32(e.bytesP2p),
												null != e.bytesP2pUpload &&
													Object.hasOwnProperty.call(e, "bytesP2pUpload") &&
													t.uint32(24).uint32(e.bytesP2pUpload),
												null != e.timespentCdn &&
													Object.hasOwnProperty.call(e, "timespentCdn") &&
													t.uint32(32).uint32(e.timespentCdn),
												null != e.timespentP2p &&
													Object.hasOwnProperty.call(e, "timespentP2p") &&
													t.uint32(40).uint32(e.timespentP2p),
												null != e.timespentP2pUpload &&
													Object.hasOwnProperty.call(e, "timespentP2pUpload") &&
													t.uint32(48).uint32(e.timespentP2pUpload),
												null != e.cntCdn &&
													Object.hasOwnProperty.call(e, "cntCdn") &&
													t.uint32(56).uint32(e.cntCdn),
												null != e.cntP2p &&
													Object.hasOwnProperty.call(e, "cntP2p") &&
													t.uint32(64).uint32(e.cntP2p),
												null != e.cntP2pUpload &&
													Object.hasOwnProperty.call(e, "cntP2pUpload") &&
													t.uint32(72).uint32(e.cntP2pUpload),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.DataStats();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.bytesCdn = e.uint32();
														break;
													case 2:
														r.bytesP2p = e.uint32();
														break;
													case 3:
														r.bytesP2pUpload = e.uint32();
														break;
													case 4:
														r.timespentCdn = e.uint32();
														break;
													case 5:
														r.timespentP2p = e.uint32();
														break;
													case 6:
														r.timespentP2pUpload = e.uint32();
														break;
													case 7:
														r.cntCdn = e.uint32();
														break;
													case 8:
														r.cntP2p = e.uint32();
														break;
													case 9:
														r.cntP2pUpload = e.uint32();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.bytesCdn &&
												  e.hasOwnProperty("bytesCdn") &&
												  !s.isInteger(e.bytesCdn)
												? "bytesCdn: integer expected"
												: null != e.bytesP2p &&
												  e.hasOwnProperty("bytesP2p") &&
												  !s.isInteger(e.bytesP2p)
												? "bytesP2p: integer expected"
												: null != e.bytesP2pUpload &&
												  e.hasOwnProperty("bytesP2pUpload") &&
												  !s.isInteger(e.bytesP2pUpload)
												? "bytesP2pUpload: integer expected"
												: null != e.timespentCdn &&
												  e.hasOwnProperty("timespentCdn") &&
												  !s.isInteger(e.timespentCdn)
												? "timespentCdn: integer expected"
												: null != e.timespentP2p &&
												  e.hasOwnProperty("timespentP2p") &&
												  !s.isInteger(e.timespentP2p)
												? "timespentP2p: integer expected"
												: null != e.timespentP2pUpload &&
												  e.hasOwnProperty("timespentP2pUpload") &&
												  !s.isInteger(e.timespentP2pUpload)
												? "timespentP2pUpload: integer expected"
												: null != e.cntCdn &&
												  e.hasOwnProperty("cntCdn") &&
												  !s.isInteger(e.cntCdn)
												? "cntCdn: integer expected"
												: null != e.cntP2p &&
												  e.hasOwnProperty("cntP2p") &&
												  !s.isInteger(e.cntP2p)
												? "cntP2p: integer expected"
												: null != e.cntP2pUpload &&
												  e.hasOwnProperty("cntP2pUpload") &&
												  !s.isInteger(e.cntP2pUpload)
												? "cntP2pUpload: integer expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.DataStats) return e;
											var t = new a.DataStats();
											return (
												null != e.bytesCdn && (t.bytesCdn = e.bytesCdn >>> 0),
												null != e.bytesP2p && (t.bytesP2p = e.bytesP2p >>> 0),
												null != e.bytesP2pUpload &&
													(t.bytesP2pUpload = e.bytesP2pUpload >>> 0),
												null != e.timespentCdn &&
													(t.timespentCdn = e.timespentCdn >>> 0),
												null != e.timespentP2p &&
													(t.timespentP2p = e.timespentP2p >>> 0),
												null != e.timespentP2pUpload &&
													(t.timespentP2pUpload = e.timespentP2pUpload >>> 0),
												null != e.cntCdn && (t.cntCdn = e.cntCdn >>> 0),
												null != e.cntP2p && (t.cntP2p = e.cntP2p >>> 0),
												null != e.cntP2pUpload &&
													(t.cntP2pUpload = e.cntP2pUpload >>> 0),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											return (
												t.defaults &&
													((n.bytesCdn = 0),
													(n.bytesP2p = 0),
													(n.bytesP2pUpload = 0),
													(n.timespentCdn = 0),
													(n.timespentP2p = 0),
													(n.timespentP2pUpload = 0),
													(n.cntCdn = 0),
													(n.cntP2p = 0),
													(n.cntP2pUpload = 0)),
												null != e.bytesCdn &&
													e.hasOwnProperty("bytesCdn") &&
													(n.bytesCdn = e.bytesCdn),
												null != e.bytesP2p &&
													e.hasOwnProperty("bytesP2p") &&
													(n.bytesP2p = e.bytesP2p),
												null != e.bytesP2pUpload &&
													e.hasOwnProperty("bytesP2pUpload") &&
													(n.bytesP2pUpload = e.bytesP2pUpload),
												null != e.timespentCdn &&
													e.hasOwnProperty("timespentCdn") &&
													(n.timespentCdn = e.timespentCdn),
												null != e.timespentP2p &&
													e.hasOwnProperty("timespentP2p") &&
													(n.timespentP2p = e.timespentP2p),
												null != e.timespentP2pUpload &&
													e.hasOwnProperty("timespentP2pUpload") &&
													(n.timespentP2pUpload = e.timespentP2pUpload),
												null != e.cntCdn &&
													e.hasOwnProperty("cntCdn") &&
													(n.cntCdn = e.cntCdn),
												null != e.cntP2p &&
													e.hasOwnProperty("cntP2p") &&
													(n.cntP2p = e.cntP2p),
												null != e.cntP2pUpload &&
													e.hasOwnProperty("cntP2pUpload") &&
													(n.cntP2pUpload = e.cntP2pUpload),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.P2PStats = (function () {
									function e(e) {
										if (
											((this.leechers = []),
											(this.seeders = []),
											(this.delays = []),
											e)
										)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.leechers = s.emptyArray),
										(e.prototype.seeders = s.emptyArray),
										(e.prototype.cntLeechers = 0),
										(e.prototype.cntSeeders = 0),
										(e.prototype.delays = s.emptyArray),
										(e.prototype.cntActiveChunks = 0),
										(e.prototype.avgNumOffer = 0),
										(e.prototype.stdNumOffer = 0),
										(e.prototype.cntConnected = 0),
										(e.prototype.cntConnectErr = 0),
										(e.prototype.cntDisconnect = 0),
										(e.prototype.cntDisconnectPp = 0),
										(e.prototype.cntChnSwitch = 0),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											if (
												(t || (t = o.create()),
												null != e.leechers && e.leechers.length)
											)
												for (var n = 0; n < e.leechers.length; ++n)
													a.PeerMetrics.encode(
														e.leechers[n],
														t.uint32(10).fork()
													).ldelim();
											if (null != e.seeders && e.seeders.length)
												for (n = 0; n < e.seeders.length; ++n)
													a.PeerMetrics.encode(
														e.seeders[n],
														t.uint32(18).fork()
													).ldelim();
											if (
												(null != e.cntLeechers &&
													Object.hasOwnProperty.call(e, "cntLeechers") &&
													t.uint32(24).uint32(e.cntLeechers),
												null != e.cntSeeders &&
													Object.hasOwnProperty.call(e, "cntSeeders") &&
													t.uint32(32).uint32(e.cntSeeders),
												null != e.delays && e.delays.length)
											)
												for (n = 0; n < e.delays.length; ++n)
													a.PeerDelay.encode(
														e.delays[n],
														t.uint32(42).fork()
													).ldelim();
											return (
												null != e.cntActiveChunks &&
													Object.hasOwnProperty.call(e, "cntActiveChunks") &&
													t.uint32(48).uint32(e.cntActiveChunks),
												null != e.avgNumOffer &&
													Object.hasOwnProperty.call(e, "avgNumOffer") &&
													t.uint32(61).float(e.avgNumOffer),
												null != e.stdNumOffer &&
													Object.hasOwnProperty.call(e, "stdNumOffer") &&
													t.uint32(69).float(e.stdNumOffer),
												null != e.cntConnected &&
													Object.hasOwnProperty.call(e, "cntConnected") &&
													t.uint32(72).uint32(e.cntConnected),
												null != e.cntConnectErr &&
													Object.hasOwnProperty.call(e, "cntConnectErr") &&
													t.uint32(80).uint32(e.cntConnectErr),
												null != e.cntDisconnect &&
													Object.hasOwnProperty.call(e, "cntDisconnect") &&
													t.uint32(88).uint32(e.cntDisconnect),
												null != e.cntDisconnectPp &&
													Object.hasOwnProperty.call(e, "cntDisconnectPp") &&
													t.uint32(96).uint32(e.cntDisconnectPp),
												null != e.cntChnSwitch &&
													Object.hasOwnProperty.call(e, "cntChnSwitch") &&
													t.uint32(104).uint32(e.cntChnSwitch),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.P2PStats();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														(r.leechers && r.leechers.length) ||
															(r.leechers = []),
															r.leechers.push(
																a.PeerMetrics.decode(e, e.uint32())
															);
														break;
													case 2:
														(r.seeders && r.seeders.length) || (r.seeders = []),
															r.seeders.push(
																a.PeerMetrics.decode(e, e.uint32())
															);
														break;
													case 3:
														r.cntLeechers = e.uint32();
														break;
													case 4:
														r.cntSeeders = e.uint32();
														break;
													case 5:
														(r.delays && r.delays.length) || (r.delays = []),
															r.delays.push(a.PeerDelay.decode(e, e.uint32()));
														break;
													case 6:
														r.cntActiveChunks = e.uint32();
														break;
													case 7:
														r.avgNumOffer = e.float();
														break;
													case 8:
														r.stdNumOffer = e.float();
														break;
													case 9:
														r.cntConnected = e.uint32();
														break;
													case 10:
														r.cntConnectErr = e.uint32();
														break;
													case 11:
														r.cntDisconnect = e.uint32();
														break;
													case 12:
														r.cntDisconnectPp = e.uint32();
														break;
													case 13:
														r.cntChnSwitch = e.uint32();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											if ("object" != typeof e || null === e)
												return "object expected";
											if (null != e.leechers && e.hasOwnProperty("leechers")) {
												if (!Array.isArray(e.leechers))
													return "leechers: array expected";
												for (var t = 0; t < e.leechers.length; ++t)
													if ((n = a.PeerMetrics.verify(e.leechers[t])))
														return "leechers." + n;
											}
											if (null != e.seeders && e.hasOwnProperty("seeders")) {
												if (!Array.isArray(e.seeders))
													return "seeders: array expected";
												for (t = 0; t < e.seeders.length; ++t)
													if ((n = a.PeerMetrics.verify(e.seeders[t])))
														return "seeders." + n;
											}
											if (
												null != e.cntLeechers &&
												e.hasOwnProperty("cntLeechers") &&
												!s.isInteger(e.cntLeechers)
											)
												return "cntLeechers: integer expected";
											if (
												null != e.cntSeeders &&
												e.hasOwnProperty("cntSeeders") &&
												!s.isInteger(e.cntSeeders)
											)
												return "cntSeeders: integer expected";
											if (null != e.delays && e.hasOwnProperty("delays")) {
												if (!Array.isArray(e.delays))
													return "delays: array expected";
												for (t = 0; t < e.delays.length; ++t) {
													var n;
													if ((n = a.PeerDelay.verify(e.delays[t])))
														return "delays." + n;
												}
											}
											return null != e.cntActiveChunks &&
												e.hasOwnProperty("cntActiveChunks") &&
												!s.isInteger(e.cntActiveChunks)
												? "cntActiveChunks: integer expected"
												: null != e.avgNumOffer &&
												  e.hasOwnProperty("avgNumOffer") &&
												  "number" != typeof e.avgNumOffer
												? "avgNumOffer: number expected"
												: null != e.stdNumOffer &&
												  e.hasOwnProperty("stdNumOffer") &&
												  "number" != typeof e.stdNumOffer
												? "stdNumOffer: number expected"
												: null != e.cntConnected &&
												  e.hasOwnProperty("cntConnected") &&
												  !s.isInteger(e.cntConnected)
												? "cntConnected: integer expected"
												: null != e.cntConnectErr &&
												  e.hasOwnProperty("cntConnectErr") &&
												  !s.isInteger(e.cntConnectErr)
												? "cntConnectErr: integer expected"
												: null != e.cntDisconnect &&
												  e.hasOwnProperty("cntDisconnect") &&
												  !s.isInteger(e.cntDisconnect)
												? "cntDisconnect: integer expected"
												: null != e.cntDisconnectPp &&
												  e.hasOwnProperty("cntDisconnectPp") &&
												  !s.isInteger(e.cntDisconnectPp)
												? "cntDisconnectPp: integer expected"
												: null != e.cntChnSwitch &&
												  e.hasOwnProperty("cntChnSwitch") &&
												  !s.isInteger(e.cntChnSwitch)
												? "cntChnSwitch: integer expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.P2PStats) return e;
											var t = new a.P2PStats();
											if (e.leechers) {
												if (!Array.isArray(e.leechers))
													throw TypeError(".P2PStats.leechers: array expected");
												t.leechers = [];
												for (var n = 0; n < e.leechers.length; ++n) {
													if ("object" != typeof e.leechers[n])
														throw TypeError(
															".P2PStats.leechers: object expected"
														);
													t.leechers[n] = a.PeerMetrics.fromObject(
														e.leechers[n]
													);
												}
											}
											if (e.seeders) {
												if (!Array.isArray(e.seeders))
													throw TypeError(".P2PStats.seeders: array expected");
												for (t.seeders = [], n = 0; n < e.seeders.length; ++n) {
													if ("object" != typeof e.seeders[n])
														throw TypeError(
															".P2PStats.seeders: object expected"
														);
													t.seeders[n] = a.PeerMetrics.fromObject(e.seeders[n]);
												}
											}
											if (
												(null != e.cntLeechers &&
													(t.cntLeechers = e.cntLeechers >>> 0),
												null != e.cntSeeders &&
													(t.cntSeeders = e.cntSeeders >>> 0),
												e.delays)
											) {
												if (!Array.isArray(e.delays))
													throw TypeError(".P2PStats.delays: array expected");
												for (t.delays = [], n = 0; n < e.delays.length; ++n) {
													if ("object" != typeof e.delays[n])
														throw TypeError(
															".P2PStats.delays: object expected"
														);
													t.delays[n] = a.PeerDelay.fromObject(e.delays[n]);
												}
											}
											return (
												null != e.cntActiveChunks &&
													(t.cntActiveChunks = e.cntActiveChunks >>> 0),
												null != e.avgNumOffer &&
													(t.avgNumOffer = Number(e.avgNumOffer)),
												null != e.stdNumOffer &&
													(t.stdNumOffer = Number(e.stdNumOffer)),
												null != e.cntConnected &&
													(t.cntConnected = e.cntConnected >>> 0),
												null != e.cntConnectErr &&
													(t.cntConnectErr = e.cntConnectErr >>> 0),
												null != e.cntDisconnect &&
													(t.cntDisconnect = e.cntDisconnect >>> 0),
												null != e.cntDisconnectPp &&
													(t.cntDisconnectPp = e.cntDisconnectPp >>> 0),
												null != e.cntChnSwitch &&
													(t.cntChnSwitch = e.cntChnSwitch >>> 0),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											if (
												((t.arrays || t.defaults) &&
													((n.leechers = []),
													(n.seeders = []),
													(n.delays = [])),
												t.defaults &&
													((n.cntLeechers = 0),
													(n.cntSeeders = 0),
													(n.cntActiveChunks = 0),
													(n.avgNumOffer = 0),
													(n.stdNumOffer = 0),
													(n.cntConnected = 0),
													(n.cntConnectErr = 0),
													(n.cntDisconnect = 0),
													(n.cntDisconnectPp = 0),
													(n.cntChnSwitch = 0)),
												e.leechers && e.leechers.length)
											) {
												n.leechers = [];
												for (var r = 0; r < e.leechers.length; ++r)
													n.leechers[r] = a.PeerMetrics.toObject(
														e.leechers[r],
														t
													);
											}
											if (e.seeders && e.seeders.length)
												for (n.seeders = [], r = 0; r < e.seeders.length; ++r)
													n.seeders[r] = a.PeerMetrics.toObject(
														e.seeders[r],
														t
													);
											if (
												(null != e.cntLeechers &&
													e.hasOwnProperty("cntLeechers") &&
													(n.cntLeechers = e.cntLeechers),
												null != e.cntSeeders &&
													e.hasOwnProperty("cntSeeders") &&
													(n.cntSeeders = e.cntSeeders),
												e.delays && e.delays.length)
											)
												for (n.delays = [], r = 0; r < e.delays.length; ++r)
													n.delays[r] = a.PeerDelay.toObject(e.delays[r], t);
											return (
												null != e.cntActiveChunks &&
													e.hasOwnProperty("cntActiveChunks") &&
													(n.cntActiveChunks = e.cntActiveChunks),
												null != e.avgNumOffer &&
													e.hasOwnProperty("avgNumOffer") &&
													(n.avgNumOffer =
														t.json && !isFinite(e.avgNumOffer)
															? String(e.avgNumOffer)
															: e.avgNumOffer),
												null != e.stdNumOffer &&
													e.hasOwnProperty("stdNumOffer") &&
													(n.stdNumOffer =
														t.json && !isFinite(e.stdNumOffer)
															? String(e.stdNumOffer)
															: e.stdNumOffer),
												null != e.cntConnected &&
													e.hasOwnProperty("cntConnected") &&
													(n.cntConnected = e.cntConnected),
												null != e.cntConnectErr &&
													e.hasOwnProperty("cntConnectErr") &&
													(n.cntConnectErr = e.cntConnectErr),
												null != e.cntDisconnect &&
													e.hasOwnProperty("cntDisconnect") &&
													(n.cntDisconnect = e.cntDisconnect),
												null != e.cntDisconnectPp &&
													e.hasOwnProperty("cntDisconnectPp") &&
													(n.cntDisconnectPp = e.cntDisconnectPp),
												null != e.cntChnSwitch &&
													e.hasOwnProperty("cntChnSwitch") &&
													(n.cntChnSwitch = e.cntChnSwitch),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.QoEStats = (function () {
									function e(e) {
										if (((this.qualityChkCnt = []), e))
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.startupTime = 0),
										(e.prototype.rebufferTime = 0),
										(e.prototype.rebufferCnt = 0),
										(e.prototype.watchingTime = 0),
										(e.prototype.bufferLength = 0),
										(e.prototype.switchUp = 0),
										(e.prototype.switchDown = 0),
										(e.prototype.qualityChkCnt = s.emptyArray),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											if (
												(t || (t = o.create()),
												null != e.startupTime &&
													Object.hasOwnProperty.call(e, "startupTime") &&
													t.uint32(13).float(e.startupTime),
												null != e.rebufferTime &&
													Object.hasOwnProperty.call(e, "rebufferTime") &&
													t.uint32(21).float(e.rebufferTime),
												null != e.rebufferCnt &&
													Object.hasOwnProperty.call(e, "rebufferCnt") &&
													t.uint32(29).float(e.rebufferCnt),
												null != e.watchingTime &&
													Object.hasOwnProperty.call(e, "watchingTime") &&
													t.uint32(37).float(e.watchingTime),
												null != e.bufferLength &&
													Object.hasOwnProperty.call(e, "bufferLength") &&
													t.uint32(45).float(e.bufferLength),
												null != e.switchUp &&
													Object.hasOwnProperty.call(e, "switchUp") &&
													t.uint32(53).float(e.switchUp),
												null != e.switchDown &&
													Object.hasOwnProperty.call(e, "switchDown") &&
													t.uint32(61).float(e.switchDown),
												null != e.qualityChkCnt && e.qualityChkCnt.length)
											) {
												t.uint32(66).fork();
												for (var n = 0; n < e.qualityChkCnt.length; ++n)
													t.uint32(e.qualityChkCnt[n]);
												t.ldelim();
											}
											return t;
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.QoEStats();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.startupTime = e.float();
														break;
													case 2:
														r.rebufferTime = e.float();
														break;
													case 3:
														r.rebufferCnt = e.float();
														break;
													case 4:
														r.watchingTime = e.float();
														break;
													case 5:
														r.bufferLength = e.float();
														break;
													case 6:
														r.switchUp = e.float();
														break;
													case 7:
														r.switchDown = e.float();
														break;
													case 8:
														if (
															((r.qualityChkCnt && r.qualityChkCnt.length) ||
																(r.qualityChkCnt = []),
															2 == (7 & o))
														)
															for (var s = e.uint32() + e.pos; e.pos < s; )
																r.qualityChkCnt.push(e.uint32());
														else r.qualityChkCnt.push(e.uint32());
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											if ("object" != typeof e || null === e)
												return "object expected";
											if (
												null != e.startupTime &&
												e.hasOwnProperty("startupTime") &&
												"number" != typeof e.startupTime
											)
												return "startupTime: number expected";
											if (
												null != e.rebufferTime &&
												e.hasOwnProperty("rebufferTime") &&
												"number" != typeof e.rebufferTime
											)
												return "rebufferTime: number expected";
											if (
												null != e.rebufferCnt &&
												e.hasOwnProperty("rebufferCnt") &&
												"number" != typeof e.rebufferCnt
											)
												return "rebufferCnt: number expected";
											if (
												null != e.watchingTime &&
												e.hasOwnProperty("watchingTime") &&
												"number" != typeof e.watchingTime
											)
												return "watchingTime: number expected";
											if (
												null != e.bufferLength &&
												e.hasOwnProperty("bufferLength") &&
												"number" != typeof e.bufferLength
											)
												return "bufferLength: number expected";
											if (
												null != e.switchUp &&
												e.hasOwnProperty("switchUp") &&
												"number" != typeof e.switchUp
											)
												return "switchUp: number expected";
											if (
												null != e.switchDown &&
												e.hasOwnProperty("switchDown") &&
												"number" != typeof e.switchDown
											)
												return "switchDown: number expected";
											if (
												null != e.qualityChkCnt &&
												e.hasOwnProperty("qualityChkCnt")
											) {
												if (!Array.isArray(e.qualityChkCnt))
													return "qualityChkCnt: array expected";
												for (var t = 0; t < e.qualityChkCnt.length; ++t)
													if (!s.isInteger(e.qualityChkCnt[t]))
														return "qualityChkCnt: integer[] expected";
											}
											return null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.QoEStats) return e;
											var t = new a.QoEStats();
											if (
												(null != e.startupTime &&
													(t.startupTime = Number(e.startupTime)),
												null != e.rebufferTime &&
													(t.rebufferTime = Number(e.rebufferTime)),
												null != e.rebufferCnt &&
													(t.rebufferCnt = Number(e.rebufferCnt)),
												null != e.watchingTime &&
													(t.watchingTime = Number(e.watchingTime)),
												null != e.bufferLength &&
													(t.bufferLength = Number(e.bufferLength)),
												null != e.switchUp && (t.switchUp = Number(e.switchUp)),
												null != e.switchDown &&
													(t.switchDown = Number(e.switchDown)),
												e.qualityChkCnt)
											) {
												if (!Array.isArray(e.qualityChkCnt))
													throw TypeError(
														".QoEStats.qualityChkCnt: array expected"
													);
												t.qualityChkCnt = [];
												for (var n = 0; n < e.qualityChkCnt.length; ++n)
													t.qualityChkCnt[n] = e.qualityChkCnt[n] >>> 0;
											}
											return t;
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											if (
												((t.arrays || t.defaults) && (n.qualityChkCnt = []),
												t.defaults &&
													((n.startupTime = 0),
													(n.rebufferTime = 0),
													(n.rebufferCnt = 0),
													(n.watchingTime = 0),
													(n.bufferLength = 0),
													(n.switchUp = 0),
													(n.switchDown = 0)),
												null != e.startupTime &&
													e.hasOwnProperty("startupTime") &&
													(n.startupTime =
														t.json && !isFinite(e.startupTime)
															? String(e.startupTime)
															: e.startupTime),
												null != e.rebufferTime &&
													e.hasOwnProperty("rebufferTime") &&
													(n.rebufferTime =
														t.json && !isFinite(e.rebufferTime)
															? String(e.rebufferTime)
															: e.rebufferTime),
												null != e.rebufferCnt &&
													e.hasOwnProperty("rebufferCnt") &&
													(n.rebufferCnt =
														t.json && !isFinite(e.rebufferCnt)
															? String(e.rebufferCnt)
															: e.rebufferCnt),
												null != e.watchingTime &&
													e.hasOwnProperty("watchingTime") &&
													(n.watchingTime =
														t.json && !isFinite(e.watchingTime)
															? String(e.watchingTime)
															: e.watchingTime),
												null != e.bufferLength &&
													e.hasOwnProperty("bufferLength") &&
													(n.bufferLength =
														t.json && !isFinite(e.bufferLength)
															? String(e.bufferLength)
															: e.bufferLength),
												null != e.switchUp &&
													e.hasOwnProperty("switchUp") &&
													(n.switchUp =
														t.json && !isFinite(e.switchUp)
															? String(e.switchUp)
															: e.switchUp),
												null != e.switchDown &&
													e.hasOwnProperty("switchDown") &&
													(n.switchDown =
														t.json && !isFinite(e.switchDown)
															? String(e.switchDown)
															: e.switchDown),
												e.qualityChkCnt && e.qualityChkCnt.length)
											) {
												n.qualityChkCnt = [];
												for (var r = 0; r < e.qualityChkCnt.length; ++r)
													n.qualityChkCnt[r] = e.qualityChkCnt[r];
											}
											return n;
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.DeviceStats = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.batteryLevel = 0),
										(e.prototype.totalMemory = s.Long
											? s.Long.fromBits(0, 0, !0)
											: 0),
										(e.prototype.usedMemory = s.Long
											? s.Long.fromBits(0, 0, !0)
											: 0),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.batteryLevel &&
													Object.hasOwnProperty.call(e, "batteryLevel") &&
													t.uint32(13).float(e.batteryLevel),
												null != e.totalMemory &&
													Object.hasOwnProperty.call(e, "totalMemory") &&
													t.uint32(16).uint64(e.totalMemory),
												null != e.usedMemory &&
													Object.hasOwnProperty.call(e, "usedMemory") &&
													t.uint32(24).uint64(e.usedMemory),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.DeviceStats();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.batteryLevel = e.float();
														break;
													case 2:
														r.totalMemory = e.uint64();
														break;
													case 3:
														r.usedMemory = e.uint64();
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.batteryLevel &&
												  e.hasOwnProperty("batteryLevel") &&
												  "number" != typeof e.batteryLevel
												? "batteryLevel: number expected"
												: null != e.totalMemory &&
												  e.hasOwnProperty("totalMemory") &&
												  !(
														s.isInteger(e.totalMemory) ||
														(e.totalMemory &&
															s.isInteger(e.totalMemory.low) &&
															s.isInteger(e.totalMemory.high))
												  )
												? "totalMemory: integer|Long expected"
												: null != e.usedMemory &&
												  e.hasOwnProperty("usedMemory") &&
												  !(
														s.isInteger(e.usedMemory) ||
														(e.usedMemory &&
															s.isInteger(e.usedMemory.low) &&
															s.isInteger(e.usedMemory.high))
												  )
												? "usedMemory: integer|Long expected"
												: null;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.DeviceStats) return e;
											var t = new a.DeviceStats();
											return (
												null != e.batteryLevel &&
													(t.batteryLevel = Number(e.batteryLevel)),
												null != e.totalMemory &&
													(s.Long
														? ((t.totalMemory = s.Long.fromValue(
																e.totalMemory
														  )).unsigned = !0)
														: "string" == typeof e.totalMemory
														? (t.totalMemory = parseInt(e.totalMemory, 10))
														: "number" == typeof e.totalMemory
														? (t.totalMemory = e.totalMemory)
														: "object" == typeof e.totalMemory &&
														  (t.totalMemory = new s.LongBits(
																e.totalMemory.low >>> 0,
																e.totalMemory.high >>> 0
														  ).toNumber(!0))),
												null != e.usedMemory &&
													(s.Long
														? ((t.usedMemory = s.Long.fromValue(
																e.usedMemory
														  )).unsigned = !0)
														: "string" == typeof e.usedMemory
														? (t.usedMemory = parseInt(e.usedMemory, 10))
														: "number" == typeof e.usedMemory
														? (t.usedMemory = e.usedMemory)
														: "object" == typeof e.usedMemory &&
														  (t.usedMemory = new s.LongBits(
																e.usedMemory.low >>> 0,
																e.usedMemory.high >>> 0
														  ).toNumber(!0))),
												t
											);
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											if (t.defaults) {
												if (((n.batteryLevel = 0), s.Long)) {
													var r = new s.Long(0, 0, !0);
													n.totalMemory =
														t.longs === String
															? r.toString()
															: t.longs === Number
															? r.toNumber()
															: r;
												} else n.totalMemory = t.longs === String ? "0" : 0;
												s.Long
													? ((r = new s.Long(0, 0, !0)),
													  (n.usedMemory =
															t.longs === String
																? r.toString()
																: t.longs === Number
																? r.toNumber()
																: r))
													: (n.usedMemory = t.longs === String ? "0" : 0);
											}
											return (
												null != e.batteryLevel &&
													e.hasOwnProperty("batteryLevel") &&
													(n.batteryLevel =
														t.json && !isFinite(e.batteryLevel)
															? String(e.batteryLevel)
															: e.batteryLevel),
												null != e.totalMemory &&
													e.hasOwnProperty("totalMemory") &&
													("number" == typeof e.totalMemory
														? (n.totalMemory =
																t.longs === String
																	? String(e.totalMemory)
																	: e.totalMemory)
														: (n.totalMemory =
																t.longs === String
																	? s.Long.prototype.toString.call(
																			e.totalMemory
																	  )
																	: t.longs === Number
																	? new s.LongBits(
																			e.totalMemory.low >>> 0,
																			e.totalMemory.high >>> 0
																	  ).toNumber(!0)
																	: e.totalMemory)),
												null != e.usedMemory &&
													e.hasOwnProperty("usedMemory") &&
													("number" == typeof e.usedMemory
														? (n.usedMemory =
																t.longs === String
																	? String(e.usedMemory)
																	: e.usedMemory)
														: (n.usedMemory =
																t.longs === String
																	? s.Long.prototype.toString.call(e.usedMemory)
																	: t.longs === Number
																	? new s.LongBits(
																			e.usedMemory.low >>> 0,
																			e.usedMemory.high >>> 0
																	  ).toNumber(!0)
																	: e.usedMemory)),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(a.Stats = (function () {
									function e(e) {
										if (e)
											for (var t = Object.keys(e), n = 0; n < t.length; ++n)
												null != e[t[n]] && (this[t[n]] = e[t[n]]);
									}
									return (
										(e.prototype.agent = null),
										(e.prototype.ts = s.Long ? s.Long.fromBits(0, 0, !1) : 0),
										(e.prototype.data = null),
										(e.prototype.qoe = null),
										(e.prototype.mediaMeta = null),
										(e.prototype.p2p = null),
										(e.prototype.player = null),
										(e.prototype.device = null),
										(e.create = function (t) {
											return new e(t);
										}),
										(e.encode = function (e, t) {
											return (
												t || (t = o.create()),
												null != e.agent &&
													Object.hasOwnProperty.call(e, "agent") &&
													a.AgentInfo.encode(
														e.agent,
														t.uint32(10).fork()
													).ldelim(),
												null != e.ts &&
													Object.hasOwnProperty.call(e, "ts") &&
													t.uint32(16).int64(e.ts),
												null != e.data &&
													Object.hasOwnProperty.call(e, "data") &&
													a.DataStats.encode(
														e.data,
														t.uint32(26).fork()
													).ldelim(),
												null != e.qoe &&
													Object.hasOwnProperty.call(e, "qoe") &&
													a.QoEStats.encode(
														e.qoe,
														t.uint32(34).fork()
													).ldelim(),
												null != e.mediaMeta &&
													Object.hasOwnProperty.call(e, "mediaMeta") &&
													a.MediaMetadata.encode(
														e.mediaMeta,
														t.uint32(42).fork()
													).ldelim(),
												null != e.p2p &&
													Object.hasOwnProperty.call(e, "p2p") &&
													a.P2PStats.encode(
														e.p2p,
														t.uint32(50).fork()
													).ldelim(),
												null != e.player &&
													Object.hasOwnProperty.call(e, "player") &&
													a.PlayerStats.encode(
														e.player,
														t.uint32(58).fork()
													).ldelim(),
												null != e.device &&
													Object.hasOwnProperty.call(e, "device") &&
													a.DeviceStats.encode(
														e.device,
														t.uint32(66).fork()
													).ldelim(),
												t
											);
										}),
										(e.encodeDelimited = function (e, t) {
											return this.encode(e, t).ldelim();
										}),
										(e.decode = function (e, t) {
											e instanceof i || (e = i.create(e));
											for (
												var n = void 0 === t ? e.len : e.pos + t,
													r = new a.Stats();
												e.pos < n;

											) {
												var o = e.uint32();
												switch (o >>> 3) {
													case 1:
														r.agent = a.AgentInfo.decode(e, e.uint32());
														break;
													case 2:
														r.ts = e.int64();
														break;
													case 3:
														r.data = a.DataStats.decode(e, e.uint32());
														break;
													case 4:
														r.qoe = a.QoEStats.decode(e, e.uint32());
														break;
													case 5:
														r.mediaMeta = a.MediaMetadata.decode(e, e.uint32());
														break;
													case 6:
														r.p2p = a.P2PStats.decode(e, e.uint32());
														break;
													case 7:
														r.player = a.PlayerStats.decode(e, e.uint32());
														break;
													case 8:
														r.device = a.DeviceStats.decode(e, e.uint32());
														break;
													default:
														e.skipType(7 & o);
												}
											}
											return r;
										}),
										(e.decodeDelimited = function (e) {
											return (
												e instanceof i || (e = new i(e)),
												this.decode(e, e.uint32())
											);
										}),
										(e.verify = function (e) {
											return "object" != typeof e || null === e
												? "object expected"
												: null != e.agent &&
												  e.hasOwnProperty("agent") &&
												  (t = a.AgentInfo.verify(e.agent))
												? "agent." + t
												: null != e.ts &&
												  e.hasOwnProperty("ts") &&
												  !(
														s.isInteger(e.ts) ||
														(e.ts &&
															s.isInteger(e.ts.low) &&
															s.isInteger(e.ts.high))
												  )
												? "ts: integer|Long expected"
												: null != e.data &&
												  e.hasOwnProperty("data") &&
												  (t = a.DataStats.verify(e.data))
												? "data." + t
												: null != e.qoe &&
												  e.hasOwnProperty("qoe") &&
												  (t = a.QoEStats.verify(e.qoe))
												? "qoe." + t
												: null != e.mediaMeta &&
												  e.hasOwnProperty("mediaMeta") &&
												  (t = a.MediaMetadata.verify(e.mediaMeta))
												? "mediaMeta." + t
												: null != e.p2p &&
												  e.hasOwnProperty("p2p") &&
												  (t = a.P2PStats.verify(e.p2p))
												? "p2p." + t
												: null != e.player &&
												  e.hasOwnProperty("player") &&
												  (t = a.PlayerStats.verify(e.player))
												? "player." + t
												: null != e.device &&
												  e.hasOwnProperty("device") &&
												  (t = a.DeviceStats.verify(e.device))
												? "device." + t
												: null;
											var t;
										}),
										(e.fromObject = function (e) {
											if (e instanceof a.Stats) return e;
											var t = new a.Stats();
											if (null != e.agent) {
												if ("object" != typeof e.agent)
													throw TypeError(".Stats.agent: object expected");
												t.agent = a.AgentInfo.fromObject(e.agent);
											}
											if (
												(null != e.ts &&
													(s.Long
														? ((t.ts = s.Long.fromValue(e.ts)).unsigned = !1)
														: "string" == typeof e.ts
														? (t.ts = parseInt(e.ts, 10))
														: "number" == typeof e.ts
														? (t.ts = e.ts)
														: "object" == typeof e.ts &&
														  (t.ts = new s.LongBits(
																e.ts.low >>> 0,
																e.ts.high >>> 0
														  ).toNumber())),
												null != e.data)
											) {
												if ("object" != typeof e.data)
													throw TypeError(".Stats.data: object expected");
												t.data = a.DataStats.fromObject(e.data);
											}
											if (null != e.qoe) {
												if ("object" != typeof e.qoe)
													throw TypeError(".Stats.qoe: object expected");
												t.qoe = a.QoEStats.fromObject(e.qoe);
											}
											if (null != e.mediaMeta) {
												if ("object" != typeof e.mediaMeta)
													throw TypeError(".Stats.mediaMeta: object expected");
												t.mediaMeta = a.MediaMetadata.fromObject(e.mediaMeta);
											}
											if (null != e.p2p) {
												if ("object" != typeof e.p2p)
													throw TypeError(".Stats.p2p: object expected");
												t.p2p = a.P2PStats.fromObject(e.p2p);
											}
											if (null != e.player) {
												if ("object" != typeof e.player)
													throw TypeError(".Stats.player: object expected");
												t.player = a.PlayerStats.fromObject(e.player);
											}
											if (null != e.device) {
												if ("object" != typeof e.device)
													throw TypeError(".Stats.device: object expected");
												t.device = a.DeviceStats.fromObject(e.device);
											}
											return t;
										}),
										(e.toObject = function (e, t) {
											t || (t = {});
											var n = {};
											if (t.defaults) {
												if (((n.agent = null), s.Long)) {
													var r = new s.Long(0, 0, !1);
													n.ts =
														t.longs === String
															? r.toString()
															: t.longs === Number
															? r.toNumber()
															: r;
												} else n.ts = t.longs === String ? "0" : 0;
												(n.data = null),
													(n.qoe = null),
													(n.mediaMeta = null),
													(n.p2p = null),
													(n.player = null),
													(n.device = null);
											}
											return (
												null != e.agent &&
													e.hasOwnProperty("agent") &&
													(n.agent = a.AgentInfo.toObject(e.agent, t)),
												null != e.ts &&
													e.hasOwnProperty("ts") &&
													("number" == typeof e.ts
														? (n.ts = t.longs === String ? String(e.ts) : e.ts)
														: (n.ts =
																t.longs === String
																	? s.Long.prototype.toString.call(e.ts)
																	: t.longs === Number
																	? new s.LongBits(
																			e.ts.low >>> 0,
																			e.ts.high >>> 0
																	  ).toNumber()
																	: e.ts)),
												null != e.data &&
													e.hasOwnProperty("data") &&
													(n.data = a.DataStats.toObject(e.data, t)),
												null != e.qoe &&
													e.hasOwnProperty("qoe") &&
													(n.qoe = a.QoEStats.toObject(e.qoe, t)),
												null != e.mediaMeta &&
													e.hasOwnProperty("mediaMeta") &&
													(n.mediaMeta = a.MediaMetadata.toObject(
														e.mediaMeta,
														t
													)),
												null != e.p2p &&
													e.hasOwnProperty("p2p") &&
													(n.p2p = a.P2PStats.toObject(e.p2p, t)),
												null != e.player &&
													e.hasOwnProperty("player") &&
													(n.player = a.PlayerStats.toObject(e.player, t)),
												null != e.device &&
													e.hasOwnProperty("device") &&
													(n.device = a.DeviceStats.toObject(e.device, t)),
												n
											);
										}),
										(e.prototype.toJSON = function () {
											return this.constructor.toObject(
												this,
												r.util.toJSONOptions
											);
										}),
										e
									);
								})()),
								(e.exports = a);
						},
						function (e, t, n) {
							"use strict";
							e.exports = f;
							var r,
								i = n(1),
								o = i.LongBits,
								s = i.base64,
								a = i.utf8;
							function u(e, t, n) {
								(this.fn = e),
									(this.len = t),
									(this.next = void 0),
									(this.val = n);
							}
							function c() {}
							function l(e) {
								(this.head = e.head),
									(this.tail = e.tail),
									(this.len = e.len),
									(this.next = e.states);
							}
							function f() {
								(this.len = 0),
									(this.head = new u(c, 0, 0)),
									(this.tail = this.head),
									(this.states = null);
							}
							var p = function () {
								return i.Buffer
									? function () {
											return (f.create = function () {
												return new r();
											})();
									  }
									: function () {
											return new f();
									  };
							};
							function h(e, t, n) {
								t[n] = 255 & e;
							}
							function g(e, t) {
								(this.len = e), (this.next = void 0), (this.val = t);
							}
							function d(e, t, n) {
								for (; e.hi; )
									(t[n++] = (127 & e.lo) | 128),
										(e.lo = ((e.lo >>> 7) | (e.hi << 25)) >>> 0),
										(e.hi >>>= 7);
								for (; e.lo > 127; )
									(t[n++] = (127 & e.lo) | 128), (e.lo = e.lo >>> 7);
								t[n++] = e.lo;
							}
							function y(e, t, n) {
								(t[n] = 255 & e),
									(t[n + 1] = (e >>> 8) & 255),
									(t[n + 2] = (e >>> 16) & 255),
									(t[n + 3] = e >>> 24);
							}
							(f.create = p()),
								(f.alloc = function (e) {
									return new i.Array(e);
								}),
								i.Array !== Array &&
									(f.alloc = i.pool(f.alloc, i.Array.prototype.subarray)),
								(f.prototype._push = function (e, t, n) {
									return (
										(this.tail = this.tail.next = new u(e, t, n)),
										(this.len += t),
										this
									);
								}),
								(g.prototype = Object.create(u.prototype)),
								(g.prototype.fn = function (e, t, n) {
									for (; e > 127; ) (t[n++] = (127 & e) | 128), (e >>>= 7);
									t[n] = e;
								}),
								(f.prototype.uint32 = function (e) {
									return (
										(this.len += (this.tail = this.tail.next =
											new g(
												(e >>>= 0) < 128
													? 1
													: e < 16384
													? 2
													: e < 2097152
													? 3
													: e < 268435456
													? 4
													: 5,
												e
											)).len),
										this
									);
								}),
								(f.prototype.int32 = function (e) {
									return e < 0
										? this._push(d, 10, o.fromNumber(e))
										: this.uint32(e);
								}),
								(f.prototype.sint32 = function (e) {
									return this.uint32(((e << 1) ^ (e >> 31)) >>> 0);
								}),
								(f.prototype.uint64 = function (e) {
									var t = o.from(e);
									return this._push(d, t.length(), t);
								}),
								(f.prototype.int64 = f.prototype.uint64),
								(f.prototype.sint64 = function (e) {
									var t = o.from(e).zzEncode();
									return this._push(d, t.length(), t);
								}),
								(f.prototype.bool = function (e) {
									return this._push(h, 1, e ? 1 : 0);
								}),
								(f.prototype.fixed32 = function (e) {
									return this._push(y, 4, e >>> 0);
								}),
								(f.prototype.sfixed32 = f.prototype.fixed32),
								(f.prototype.fixed64 = function (e) {
									var t = o.from(e);
									return this._push(y, 4, t.lo)._push(y, 4, t.hi);
								}),
								(f.prototype.sfixed64 = f.prototype.fixed64),
								(f.prototype.float = function (e) {
									return this._push(i.float.writeFloatLE, 4, e);
								}),
								(f.prototype.double = function (e) {
									return this._push(i.float.writeDoubleLE, 8, e);
								});
							var m = i.Array.prototype.set
								? function (e, t, n) {
										t.set(e, n);
								  }
								: function (e, t, n) {
										for (var r = 0; r < e.length; ++r) t[n + r] = e[r];
								  };
							(f.prototype.bytes = function (e) {
								var t = e.length >>> 0;
								if (!t) return this._push(h, 1, 0);
								if (i.isString(e)) {
									var n = f.alloc((t = s.length(e)));
									s.decode(e, n, 0), (e = n);
								}
								return this.uint32(t)._push(m, t, e);
							}),
								(f.prototype.string = function (e) {
									var t = a.length(e);
									return t
										? this.uint32(t)._push(a.write, t, e)
										: this._push(h, 1, 0);
								}),
								(f.prototype.fork = function () {
									return (
										(this.states = new l(this)),
										(this.head = this.tail = new u(c, 0, 0)),
										(this.len = 0),
										this
									);
								}),
								(f.prototype.reset = function () {
									return (
										this.states
											? ((this.head = this.states.head),
											  (this.tail = this.states.tail),
											  (this.len = this.states.len),
											  (this.states = this.states.next))
											: ((this.head = this.tail = new u(c, 0, 0)),
											  (this.len = 0)),
										this
									);
								}),
								(f.prototype.ldelim = function () {
									var e = this.head,
										t = this.tail,
										n = this.len;
									return (
										this.reset().uint32(n),
										n &&
											((this.tail.next = e.next),
											(this.tail = t),
											(this.len += n)),
										this
									);
								}),
								(f.prototype.finish = function () {
									for (
										var e = this.head.next,
											t = this.constructor.alloc(this.len),
											n = 0;
										e;

									)
										e.fn(e.val, t, n), (n += e.len), (e = e.next);
									return t;
								}),
								(f._configure = function (e) {
									(r = e), (f.create = p()), r._configure();
								});
						},
						function (e, t, n) {
							"use strict";
							e.exports = u;
							var r,
								i = n(1),
								o = i.LongBits,
								s = i.utf8;
							function a(e, t) {
								return RangeError(
									"index out of range: " +
										e.pos +
										" + " +
										(t || 1) +
										" > " +
										e.len
								);
							}
							function u(e) {
								(this.buf = e), (this.pos = 0), (this.len = e.length);
							}
							var c,
								l =
									"undefined" != typeof Uint8Array
										? function (e) {
												if (e instanceof Uint8Array || Array.isArray(e))
													return new u(e);
												throw Error("illegal buffer");
										  }
										: function (e) {
												if (Array.isArray(e)) return new u(e);
												throw Error("illegal buffer");
										  },
								f = function () {
									return i.Buffer
										? function (e) {
												return (u.create = function (e) {
													return i.Buffer.isBuffer(e) ? new r(e) : l(e);
												})(e);
										  }
										: l;
								};
							function p() {
								var e = new o(0, 0),
									t = 0;
								if (!(this.len - this.pos > 4)) {
									for (; t < 3; ++t) {
										if (this.pos >= this.len) throw a(this);
										if (
											((e.lo =
												(e.lo | ((127 & this.buf[this.pos]) << (7 * t))) >>> 0),
											this.buf[this.pos++] < 128)
										)
											return e;
									}
									return (
										(e.lo =
											(e.lo | ((127 & this.buf[this.pos++]) << (7 * t))) >>> 0),
										e
									);
								}
								for (; t < 4; ++t)
									if (
										((e.lo =
											(e.lo | ((127 & this.buf[this.pos]) << (7 * t))) >>> 0),
										this.buf[this.pos++] < 128)
									)
										return e;
								if (
									((e.lo = (e.lo | ((127 & this.buf[this.pos]) << 28)) >>> 0),
									(e.hi = (e.hi | ((127 & this.buf[this.pos]) >> 4)) >>> 0),
									this.buf[this.pos++] < 128)
								)
									return e;
								if (((t = 0), this.len - this.pos > 4)) {
									for (; t < 5; ++t)
										if (
											((e.hi =
												(e.hi | ((127 & this.buf[this.pos]) << (7 * t + 3))) >>>
												0),
											this.buf[this.pos++] < 128)
										)
											return e;
								} else
									for (; t < 5; ++t) {
										if (this.pos >= this.len) throw a(this);
										if (
											((e.hi =
												(e.hi | ((127 & this.buf[this.pos]) << (7 * t + 3))) >>>
												0),
											this.buf[this.pos++] < 128)
										)
											return e;
									}
								throw Error("invalid varint encoding");
							}
							function h(e, t) {
								return (
									(e[t - 4] |
										(e[t - 3] << 8) |
										(e[t - 2] << 16) |
										(e[t - 1] << 24)) >>>
									0
								);
							}
							function g() {
								if (this.pos + 8 > this.len) throw a(this, 8);
								return new o(
									h(this.buf, (this.pos += 4)),
									h(this.buf, (this.pos += 4))
								);
							}
							(u.create = f()),
								(u.prototype._slice =
									i.Array.prototype.subarray || i.Array.prototype.slice),
								(u.prototype.uint32 =
									((c = 4294967295),
									function () {
										if (
											((c = (127 & this.buf[this.pos]) >>> 0),
											this.buf[this.pos++] < 128)
										)
											return c;
										if (
											((c = (c | ((127 & this.buf[this.pos]) << 7)) >>> 0),
											this.buf[this.pos++] < 128)
										)
											return c;
										if (
											((c = (c | ((127 & this.buf[this.pos]) << 14)) >>> 0),
											this.buf[this.pos++] < 128)
										)
											return c;
										if (
											((c = (c | ((127 & this.buf[this.pos]) << 21)) >>> 0),
											this.buf[this.pos++] < 128)
										)
											return c;
										if (
											((c = (c | ((15 & this.buf[this.pos]) << 28)) >>> 0),
											this.buf[this.pos++] < 128)
										)
											return c;
										if ((this.pos += 5) > this.len)
											throw ((this.pos = this.len), a(this, 10));
										return c;
									})),
								(u.prototype.int32 = function () {
									return 0 | this.uint32();
								}),
								(u.prototype.sint32 = function () {
									var e = this.uint32();
									return ((e >>> 1) ^ -(1 & e)) | 0;
								}),
								(u.prototype.bool = function () {
									return 0 !== this.uint32();
								}),
								(u.prototype.fixed32 = function () {
									if (this.pos + 4 > this.len) throw a(this, 4);
									return h(this.buf, (this.pos += 4));
								}),
								(u.prototype.sfixed32 = function () {
									if (this.pos + 4 > this.len) throw a(this, 4);
									return 0 | h(this.buf, (this.pos += 4));
								}),
								(u.prototype.float = function () {
									if (this.pos + 4 > this.len) throw a(this, 4);
									var e = i.float.readFloatLE(this.buf, this.pos);
									return (this.pos += 4), e;
								}),
								(u.prototype.double = function () {
									if (this.pos + 8 > this.len) throw a(this, 4);
									var e = i.float.readDoubleLE(this.buf, this.pos);
									return (this.pos += 8), e;
								}),
								(u.prototype.bytes = function () {
									var e = this.uint32(),
										t = this.pos,
										n = this.pos + e;
									if (n > this.len) throw a(this, e);
									return (
										(this.pos += e),
										Array.isArray(this.buf)
											? this.buf.slice(t, n)
											: t === n
											? new this.buf.constructor(0)
											: this._slice.call(this.buf, t, n)
									);
								}),
								(u.prototype.string = function () {
									var e = this.bytes();
									return s.read(e, 0, e.length);
								}),
								(u.prototype.skip = function (e) {
									if ("number" == typeof e) {
										if (this.pos + e > this.len) throw a(this, e);
										this.pos += e;
									} else
										do {
											if (this.pos >= this.len) throw a(this);
										} while (128 & this.buf[this.pos++]);
									return this;
								}),
								(u.prototype.skipType = function (e) {
									switch (e) {
										case 0:
											this.skip();
											break;
										case 1:
											this.skip(8);
											break;
										case 2:
											this.skip(this.uint32());
											break;
										case 3:
											for (; 4 != (e = 7 & this.uint32()); ) this.skipType(e);
											break;
										case 5:
											this.skip(4);
											break;
										default:
											throw Error(
												"invalid wire type " + e + " at offset " + this.pos
											);
									}
									return this;
								}),
								(u._configure = function (e) {
									(r = e), (u.create = f()), r._configure();
									var t = i.Long ? "toLong" : "toNumber";
									i.merge(u.prototype, {
										int64: function () {
											return p.call(this)[t](!1);
										},
										uint64: function () {
											return p.call(this)[t](!0);
										},
										sint64: function () {
											return p.call(this).zzDecode()[t](!1);
										},
										fixed64: function () {
											return g.call(this)[t](!0);
										},
										sfixed64: function () {
											return g.call(this)[t](!1);
										},
									});
								});
						},
						function (e, t, n) {
							"use strict";
							Object.defineProperty(t, "__esModule", { value: !0 }),
								(t.newStatsServerConnector = void 0);
							var r = n(34),
								i = n(2),
								o = (function () {
									function e(e, t) {
										void 0 === t && (t = ""),
											(this.requests = e),
											(this.statsPath = t);
									}
									return (
										(e.prototype.sendStats = function (e) {
											var t = i.Stats.encode(e).finish();
											return this.requests.post(
												this.statsPath,
												t.slice().buffer
											);
										}),
										e
									);
								})();
							(t.newStatsServerConnector = function (e) {
								return new o(
									r.default.create({ baseURL: e, withCredentials: !0 }),
									"/stats"
								);
							}),
								(t.default = o);
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e, t) {
								return function () {
									for (
										var n = new Array(arguments.length), r = 0;
										r < n.length;
										r++
									)
										n[r] = arguments[r];
									return e.apply(t, n);
								};
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							function i(e) {
								return encodeURIComponent(e)
									.replace(/%3A/gi, ":")
									.replace(/%24/g, "$")
									.replace(/%2C/gi, ",")
									.replace(/%20/g, "+")
									.replace(/%5B/gi, "[")
									.replace(/%5D/gi, "]");
							}
							e.exports = function (e, t, n) {
								if (!t) return e;
								var o;
								if (n) o = n(t);
								else if (r.isURLSearchParams(t)) o = t.toString();
								else {
									var s = [];
									r.forEach(t, function (e, t) {
										null != e &&
											(r.isArray(e) ? (t += "[]") : (e = [e]),
											r.forEach(e, function (e) {
												r.isDate(e)
													? (e = e.toISOString())
													: r.isObject(e) && (e = JSON.stringify(e)),
													s.push(i(t) + "=" + i(e));
											}));
									}),
										(o = s.join("&"));
								}
								if (o) {
									var a = e.indexOf("#");
									-1 !== a && (e = e.slice(0, a)),
										(e += (-1 === e.indexOf("?") ? "?" : "&") + o);
								}
								return e;
							};
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e) {
								return !(!e || !e.__CANCEL__);
							};
						},
						function (e, t, n) {
							"use strict";
							(function (t) {
								var r = n(0),
									i = n(41),
									o = { "Content-Type": "application/x-www-form-urlencoded" };
								function s(e, t) {
									!r.isUndefined(e) &&
										r.isUndefined(e["Content-Type"]) &&
										(e["Content-Type"] = t);
								}
								var a,
									u = {
										adapter:
											(("undefined" != typeof XMLHttpRequest ||
												(void 0 !== t &&
													"[object process]" ===
														Object.prototype.toString.call(t))) &&
												(a = n(10)),
											a),
										transformRequest: [
											function (e, t) {
												return (
													i(t, "Accept"),
													i(t, "Content-Type"),
													r.isFormData(e) ||
													r.isArrayBuffer(e) ||
													r.isBuffer(e) ||
													r.isStream(e) ||
													r.isFile(e) ||
													r.isBlob(e)
														? e
														: r.isArrayBufferView(e)
														? e.buffer
														: r.isURLSearchParams(e)
														? (s(
																t,
																"application/x-www-form-urlencoded;charset=utf-8"
														  ),
														  e.toString())
														: r.isObject(e)
														? (s(t, "application/json;charset=utf-8"),
														  JSON.stringify(e))
														: e
												);
											},
										],
										transformResponse: [
											function (e) {
												if ("string" == typeof e)
													try {
														e = JSON.parse(e);
													} catch (e) {}
												return e;
											},
										],
										timeout: 0,
										xsrfCookieName: "XSRF-TOKEN",
										xsrfHeaderName: "X-XSRF-TOKEN",
										maxContentLength: -1,
										maxBodyLength: -1,
										validateStatus: function (e) {
											return e >= 200 && e < 300;
										},
										headers: {
											common: { Accept: "application/json, text/plain, */*" },
										},
									};
								r.forEach(["delete", "get", "head"], function (e) {
									u.headers[e] = {};
								}),
									r.forEach(["post", "put", "patch"], function (e) {
										u.headers[e] = r.merge(o);
									}),
									(e.exports = u);
							}).call(this, n(40));
						},
						function (e, t, n) {
							"use strict";
							var r = n(0),
								i = n(42),
								o = n(44),
								s = n(7),
								a = n(45),
								u = n(48),
								c = n(49),
								l = n(11);
							e.exports = function (e) {
								return new Promise(function (t, n) {
									var f = e.data,
										p = e.headers;
									r.isFormData(f) && delete p["Content-Type"],
										(r.isBlob(f) || r.isFile(f)) &&
											f.type &&
											delete p["Content-Type"];
									var h = new XMLHttpRequest();
									if (e.auth) {
										var g = e.auth.username || "",
											d = unescape(encodeURIComponent(e.auth.password)) || "";
										p.Authorization = "Basic " + btoa(g + ":" + d);
									}
									var y = a(e.baseURL, e.url);
									if (
										(h.open(
											e.method.toUpperCase(),
											s(y, e.params, e.paramsSerializer),
											!0
										),
										(h.timeout = e.timeout),
										(h.onreadystatechange = function () {
											if (
												h &&
												4 === h.readyState &&
												(0 !== h.status ||
													(h.responseURL &&
														0 === h.responseURL.indexOf("file:")))
											) {
												var r =
														"getAllResponseHeaders" in h
															? u(h.getAllResponseHeaders())
															: null,
													o = {
														data:
															e.responseType && "text" !== e.responseType
																? h.response
																: h.responseText,
														status: h.status,
														statusText: h.statusText,
														headers: r,
														config: e,
														request: h,
													};
												i(t, n, o), (h = null);
											}
										}),
										(h.onabort = function () {
											h &&
												(n(l("Request aborted", e, "ECONNABORTED", h)),
												(h = null));
										}),
										(h.onerror = function () {
											n(l("Network Error", e, null, h)), (h = null);
										}),
										(h.ontimeout = function () {
											var t = "timeout of " + e.timeout + "ms exceeded";
											e.timeoutErrorMessage && (t = e.timeoutErrorMessage),
												n(l(t, e, "ECONNABORTED", h)),
												(h = null);
										}),
										r.isStandardBrowserEnv())
									) {
										var m =
											(e.withCredentials || c(y)) && e.xsrfCookieName
												? o.read(e.xsrfCookieName)
												: void 0;
										m && (p[e.xsrfHeaderName] = m);
									}
									if (
										("setRequestHeader" in h &&
											r.forEach(p, function (e, t) {
												void 0 === f && "content-type" === t.toLowerCase()
													? delete p[t]
													: h.setRequestHeader(t, e);
											}),
										r.isUndefined(e.withCredentials) ||
											(h.withCredentials = !!e.withCredentials),
										e.responseType)
									)
										try {
											h.responseType = e.responseType;
										} catch (t) {
											if ("json" !== e.responseType) throw t;
										}
									"function" == typeof e.onDownloadProgress &&
										h.addEventListener("progress", e.onDownloadProgress),
										"function" == typeof e.onUploadProgress &&
											h.upload &&
											h.upload.addEventListener("progress", e.onUploadProgress),
										e.cancelToken &&
											e.cancelToken.promise.then(function (e) {
												h && (h.abort(), n(e), (h = null));
											}),
										f || (f = null),
										h.send(f);
								});
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(43);
							e.exports = function (e, t, n, i, o) {
								var s = new Error(e);
								return r(s, t, n, i, o);
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							e.exports = function (e, t) {
								t = t || {};
								var n = {},
									i = ["url", "method", "data"],
									o = ["headers", "auth", "proxy", "params"],
									s = [
										"baseURL",
										"transformRequest",
										"transformResponse",
										"paramsSerializer",
										"timeout",
										"timeoutMessage",
										"withCredentials",
										"adapter",
										"responseType",
										"xsrfCookieName",
										"xsrfHeaderName",
										"onUploadProgress",
										"onDownloadProgress",
										"decompress",
										"maxContentLength",
										"maxBodyLength",
										"maxRedirects",
										"transport",
										"httpAgent",
										"httpsAgent",
										"cancelToken",
										"socketPath",
										"responseEncoding",
									],
									a = ["validateStatus"];
								function u(e, t) {
									return r.isPlainObject(e) && r.isPlainObject(t)
										? r.merge(e, t)
										: r.isPlainObject(t)
										? r.merge({}, t)
										: r.isArray(t)
										? t.slice()
										: t;
								}
								function c(i) {
									r.isUndefined(t[i])
										? r.isUndefined(e[i]) || (n[i] = u(void 0, e[i]))
										: (n[i] = u(e[i], t[i]));
								}
								r.forEach(i, function (e) {
									r.isUndefined(t[e]) || (n[e] = u(void 0, t[e]));
								}),
									r.forEach(o, c),
									r.forEach(s, function (i) {
										r.isUndefined(t[i])
											? r.isUndefined(e[i]) || (n[i] = u(void 0, e[i]))
											: (n[i] = u(void 0, t[i]));
									}),
									r.forEach(a, function (r) {
										r in t
											? (n[r] = u(e[r], t[r]))
											: r in e && (n[r] = u(void 0, e[r]));
									});
								var l = i.concat(o).concat(s).concat(a),
									f = Object.keys(e)
										.concat(Object.keys(t))
										.filter(function (e) {
											return -1 === l.indexOf(e);
										});
								return r.forEach(f, c), n;
							};
						},
						function (e, t, n) {
							"use strict";
							function r(e) {
								this.message = e;
							}
							(r.prototype.toString = function () {
								return "Cancel" + (this.message ? ": " + this.message : "");
							}),
								(r.prototype.__CANCEL__ = !0),
								(e.exports = r);
						},
						function (e, t, n) {
							"use strict";
							var r,
								i =
									(this && this.__extends) ||
									((r = function (e, t) {
										return (r =
											Object.setPrototypeOf ||
											({ __proto__: [] } instanceof Array &&
												function (e, t) {
													e.__proto__ = t;
												}) ||
											function (e, t) {
												for (var n in t)
													Object.prototype.hasOwnProperty.call(t, n) &&
														(e[n] = t[n]);
											})(e, t);
									}),
									function (e, t) {
										function n() {
											this.constructor = e;
										}
										r(e, t),
											(e.prototype =
												null === t
													? Object.create(t)
													: ((n.prototype = t.prototype), new n()));
									});
							Object.defineProperty(t, "__esModule", { value: !0 }),
								(t.ConfigError = t.verifyConfig = void 0);
							var o = (function (e) {
								function t() {
									return (null !== e && e.apply(this, arguments)) || this;
								}
								return i(t, e), t;
							})(Error);
							(t.ConfigError = o),
								(t.verifyConfig = function (e) {
									if (!e.agentInfo) throw new o("The agentInfo is not set");
									if (!e.agentInfo.apiKey || "" == e.agentInfo.apiKey)
										throw new o("The agentInfo apiKey is not set or its empty");
									if (!e.agentInfo.contentId || "" == e.agentInfo.contentId)
										throw new o(
											"The agentInfo's contentId is not set or its empty"
										);
									if (
										null != e.mediaMetadata.videoFormat &&
										"" === e.mediaMetadata.videoFormat
									)
										throw new o("The mediaMetadata's videoFormat is not set");
									if (null != e.mediaMetadata.url)
										try {
											new URL(e.mediaMetadata.url);
										} catch (e) {
											console.warn("The url is not correct");
										}
									return !0;
								});
						},
						function (e, t, n) {
							"use strict";
							Object.defineProperty(t, "__esModule", { value: !0 }),
								(t.P2PStats =
									t.DataStats =
									t.AgentInfo =
									t.QoEStats =
									t.newStatsReporter =
									t.StatsServerConnector =
									t.StatsReporter =
										void 0);
							var r = n(2);
							Object.defineProperty(t, "AgentInfo", {
								enumerable: !0,
								get: function () {
									return r.AgentInfo;
								},
							}),
								Object.defineProperty(t, "DataStats", {
									enumerable: !0,
									get: function () {
										return r.DataStats;
									},
								}),
								Object.defineProperty(t, "P2PStats", {
									enumerable: !0,
									get: function () {
										return r.P2PStats;
									},
								}),
								Object.defineProperty(t, "QoEStats", {
									enumerable: !0,
									get: function () {
										return r.QoEStats;
									},
								});
							var i = n(32);
							(t.StatsReporter = i.default),
								Object.defineProperty(t, "newStatsReporter", {
									enumerable: !0,
									get: function () {
										return i.newStatsReporter;
									},
								});
							var o = n(5);
							t.StatsServerConnector = o.default;
						},
						function (e, t, n) {
							"use strict";
							e.exports = n(17);
						},
						function (e, t, n) {
							"use strict";
							var r = t;
							function i() {
								r.util._configure(),
									r.Writer._configure(r.BufferWriter),
									r.Reader._configure(r.BufferReader);
							}
							(r.build = "minimal"),
								(r.Writer = n(3)),
								(r.BufferWriter = n(27)),
								(r.Reader = n(4)),
								(r.BufferReader = n(28)),
								(r.util = n(1)),
								(r.rpc = n(29)),
								(r.roots = n(31)),
								(r.configure = i),
								i();
						},
						function (e, t) {
							var n;
							n = (function () {
								return this;
							})();
							try {
								n = n || new Function("return this")();
							} catch (e) {
								"object" == typeof window && (n = window);
							}
							e.exports = n;
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e, t) {
								for (
									var n = new Array(arguments.length - 1), r = 0, i = 2, o = !0;
									i < arguments.length;

								)
									n[r++] = arguments[i++];
								return new Promise(function (i, s) {
									n[r] = function (e) {
										if (o)
											if (((o = !1), e)) s(e);
											else {
												for (
													var t = new Array(arguments.length - 1), n = 0;
													n < t.length;

												)
													t[n++] = arguments[n];
												i.apply(null, t);
											}
									};
									try {
										e.apply(t || null, n);
									} catch (e) {
										o && ((o = !1), s(e));
									}
								});
							};
						},
						function (e, t, n) {
							"use strict";
							var r = t;
							r.length = function (e) {
								var t = e.length;
								if (!t) return 0;
								for (var n = 0; --t % 4 > 1 && "=" === e.charAt(t); ) ++n;
								return Math.ceil(3 * e.length) / 4 - n;
							};
							for (var i = new Array(64), o = new Array(123), s = 0; s < 64; )
								o[
									(i[s] =
										s < 26
											? s + 65
											: s < 52
											? s + 71
											: s < 62
											? s - 4
											: (s - 59) | 43)
								] = s++;
							(r.encode = function (e, t, n) {
								for (var r, o = null, s = [], a = 0, u = 0; t < n; ) {
									var c = e[t++];
									switch (u) {
										case 0:
											(s[a++] = i[c >> 2]), (r = (3 & c) << 4), (u = 1);
											break;
										case 1:
											(s[a++] = i[r | (c >> 4)]), (r = (15 & c) << 2), (u = 2);
											break;
										case 2:
											(s[a++] = i[r | (c >> 6)]), (s[a++] = i[63 & c]), (u = 0);
									}
									a > 8191 &&
										((o || (o = [])).push(String.fromCharCode.apply(String, s)),
										(a = 0));
								}
								return (
									u &&
										((s[a++] = i[r]), (s[a++] = 61), 1 === u && (s[a++] = 61)),
									o
										? (a &&
												o.push(
													String.fromCharCode.apply(String, s.slice(0, a))
												),
										  o.join(""))
										: String.fromCharCode.apply(String, s.slice(0, a))
								);
							}),
								(r.decode = function (e, t, n) {
									for (var r, i = n, s = 0, a = 0; a < e.length; ) {
										var u = e.charCodeAt(a++);
										if (61 === u && s > 1) break;
										if (void 0 === (u = o[u])) throw Error("invalid encoding");
										switch (s) {
											case 0:
												(r = u), (s = 1);
												break;
											case 1:
												(t[n++] = (r << 2) | ((48 & u) >> 4)), (r = u), (s = 2);
												break;
											case 2:
												(t[n++] = ((15 & r) << 4) | ((60 & u) >> 2)),
													(r = u),
													(s = 3);
												break;
											case 3:
												(t[n++] = ((3 & r) << 6) | u), (s = 0);
										}
									}
									if (1 === s) throw Error("invalid encoding");
									return n - i;
								}),
								(r.test = function (e) {
									return /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(
										e
									);
								});
						},
						function (e, t, n) {
							"use strict";
							function r() {
								this._listeners = {};
							}
							(e.exports = r),
								(r.prototype.on = function (e, t, n) {
									return (
										(this._listeners[e] || (this._listeners[e] = [])).push({
											fn: t,
											ctx: n || this,
										}),
										this
									);
								}),
								(r.prototype.off = function (e, t) {
									if (void 0 === e) this._listeners = {};
									else if (void 0 === t) this._listeners[e] = [];
									else
										for (var n = this._listeners[e], r = 0; r < n.length; )
											n[r].fn === t ? n.splice(r, 1) : ++r;
									return this;
								}),
								(r.prototype.emit = function (e) {
									var t = this._listeners[e];
									if (t) {
										for (var n = [], r = 1; r < arguments.length; )
											n.push(arguments[r++]);
										for (r = 0; r < t.length; ) t[r].fn.apply(t[r++].ctx, n);
									}
									return this;
								});
						},
						function (e, t, n) {
							"use strict";
							function r(e) {
								return (
									"undefined" != typeof Float32Array
										? (function () {
												var t = new Float32Array([-0]),
													n = new Uint8Array(t.buffer),
													r = 128 === n[3];
												function i(e, r, i) {
													(t[0] = e),
														(r[i] = n[0]),
														(r[i + 1] = n[1]),
														(r[i + 2] = n[2]),
														(r[i + 3] = n[3]);
												}
												function o(e, r, i) {
													(t[0] = e),
														(r[i] = n[3]),
														(r[i + 1] = n[2]),
														(r[i + 2] = n[1]),
														(r[i + 3] = n[0]);
												}
												function s(e, r) {
													return (
														(n[0] = e[r]),
														(n[1] = e[r + 1]),
														(n[2] = e[r + 2]),
														(n[3] = e[r + 3]),
														t[0]
													);
												}
												function a(e, r) {
													return (
														(n[3] = e[r]),
														(n[2] = e[r + 1]),
														(n[1] = e[r + 2]),
														(n[0] = e[r + 3]),
														t[0]
													);
												}
												(e.writeFloatLE = r ? i : o),
													(e.writeFloatBE = r ? o : i),
													(e.readFloatLE = r ? s : a),
													(e.readFloatBE = r ? a : s);
										  })()
										: (function () {
												function t(e, t, n, r) {
													var i = t < 0 ? 1 : 0;
													if ((i && (t = -t), 0 === t))
														e(1 / t > 0 ? 0 : 2147483648, n, r);
													else if (isNaN(t)) e(2143289344, n, r);
													else if (t > 34028234663852886e22)
														e(((i << 31) | 2139095040) >>> 0, n, r);
													else if (t < 11754943508222875e-54)
														e(
															((i << 31) |
																Math.round(t / 1401298464324817e-60)) >>>
																0,
															n,
															r
														);
													else {
														var o = Math.floor(Math.log(t) / Math.LN2);
														e(
															((i << 31) |
																((o + 127) << 23) |
																(8388607 &
																	Math.round(
																		t * Math.pow(2, -o) * 8388608
																	))) >>>
																0,
															n,
															r
														);
													}
												}
												function n(e, t, n) {
													var r = e(t, n),
														i = 2 * (r >> 31) + 1,
														o = (r >>> 23) & 255,
														s = 8388607 & r;
													return 255 === o
														? s
															? NaN
															: i * (1 / 0)
														: 0 === o
														? 1401298464324817e-60 * i * s
														: i * Math.pow(2, o - 150) * (s + 8388608);
												}
												(e.writeFloatLE = t.bind(null, i)),
													(e.writeFloatBE = t.bind(null, o)),
													(e.readFloatLE = n.bind(null, s)),
													(e.readFloatBE = n.bind(null, a));
										  })(),
									"undefined" != typeof Float64Array
										? (function () {
												var t = new Float64Array([-0]),
													n = new Uint8Array(t.buffer),
													r = 128 === n[7];
												function i(e, r, i) {
													(t[0] = e),
														(r[i] = n[0]),
														(r[i + 1] = n[1]),
														(r[i + 2] = n[2]),
														(r[i + 3] = n[3]),
														(r[i + 4] = n[4]),
														(r[i + 5] = n[5]),
														(r[i + 6] = n[6]),
														(r[i + 7] = n[7]);
												}
												function o(e, r, i) {
													(t[0] = e),
														(r[i] = n[7]),
														(r[i + 1] = n[6]),
														(r[i + 2] = n[5]),
														(r[i + 3] = n[4]),
														(r[i + 4] = n[3]),
														(r[i + 5] = n[2]),
														(r[i + 6] = n[1]),
														(r[i + 7] = n[0]);
												}
												function s(e, r) {
													return (
														(n[0] = e[r]),
														(n[1] = e[r + 1]),
														(n[2] = e[r + 2]),
														(n[3] = e[r + 3]),
														(n[4] = e[r + 4]),
														(n[5] = e[r + 5]),
														(n[6] = e[r + 6]),
														(n[7] = e[r + 7]),
														t[0]
													);
												}
												function a(e, r) {
													return (
														(n[7] = e[r]),
														(n[6] = e[r + 1]),
														(n[5] = e[r + 2]),
														(n[4] = e[r + 3]),
														(n[3] = e[r + 4]),
														(n[2] = e[r + 5]),
														(n[1] = e[r + 6]),
														(n[0] = e[r + 7]),
														t[0]
													);
												}
												(e.writeDoubleLE = r ? i : o),
													(e.writeDoubleBE = r ? o : i),
													(e.readDoubleLE = r ? s : a),
													(e.readDoubleBE = r ? a : s);
										  })()
										: (function () {
												function t(e, t, n, r, i, o) {
													var s = r < 0 ? 1 : 0;
													if ((s && (r = -r), 0 === r))
														e(0, i, o + t),
															e(1 / r > 0 ? 0 : 2147483648, i, o + n);
													else if (isNaN(r))
														e(0, i, o + t), e(2146959360, i, o + n);
													else if (r > 17976931348623157e292)
														e(0, i, o + t),
															e(((s << 31) | 2146435072) >>> 0, i, o + n);
													else {
														var a;
														if (r < 22250738585072014e-324)
															e((a = r / 5e-324) >>> 0, i, o + t),
																e(
																	((s << 31) | (a / 4294967296)) >>> 0,
																	i,
																	o + n
																);
														else {
															var u = Math.floor(Math.log(r) / Math.LN2);
															1024 === u && (u = 1023),
																e(
																	(4503599627370496 *
																		(a = r * Math.pow(2, -u))) >>>
																		0,
																	i,
																	o + t
																),
																e(
																	((s << 31) |
																		((u + 1023) << 20) |
																		((1048576 * a) & 1048575)) >>>
																		0,
																	i,
																	o + n
																);
														}
													}
												}
												function n(e, t, n, r, i) {
													var o = e(r, i + t),
														s = e(r, i + n),
														a = 2 * (s >> 31) + 1,
														u = (s >>> 20) & 2047,
														c = 4294967296 * (1048575 & s) + o;
													return 2047 === u
														? c
															? NaN
															: a * (1 / 0)
														: 0 === u
														? 5e-324 * a * c
														: a *
														  Math.pow(2, u - 1075) *
														  (c + 4503599627370496);
												}
												(e.writeDoubleLE = t.bind(null, i, 0, 4)),
													(e.writeDoubleBE = t.bind(null, o, 4, 0)),
													(e.readDoubleLE = n.bind(null, s, 0, 4)),
													(e.readDoubleBE = n.bind(null, a, 4, 0));
										  })(),
									e
								);
							}
							function i(e, t, n) {
								(t[n] = 255 & e),
									(t[n + 1] = (e >>> 8) & 255),
									(t[n + 2] = (e >>> 16) & 255),
									(t[n + 3] = e >>> 24);
							}
							function o(e, t, n) {
								(t[n] = e >>> 24),
									(t[n + 1] = (e >>> 16) & 255),
									(t[n + 2] = (e >>> 8) & 255),
									(t[n + 3] = 255 & e);
							}
							function s(e, t) {
								return (
									(e[t] |
										(e[t + 1] << 8) |
										(e[t + 2] << 16) |
										(e[t + 3] << 24)) >>>
									0
								);
							}
							function a(e, t) {
								return (
									((e[t] << 24) |
										(e[t + 1] << 16) |
										(e[t + 2] << 8) |
										e[t + 3]) >>>
									0
								);
							}
							e.exports = r(r);
						},
						function (module, exports, __webpack_require__) {
							"use strict";
							function inquire(moduleName) {
								try {
									var mod = eval("quire".replace(/^/, "re"))(moduleName);
									if (mod && (mod.length || Object.keys(mod).length))
										return mod;
								} catch (e) {}
								return null;
							}
							module.exports = inquire;
						},
						function (e, t, n) {
							"use strict";
							var r = t;
							(r.length = function (e) {
								for (var t = 0, n = 0, r = 0; r < e.length; ++r)
									(n = e.charCodeAt(r)) < 128
										? (t += 1)
										: n < 2048
										? (t += 2)
										: 55296 == (64512 & n) &&
										  56320 == (64512 & e.charCodeAt(r + 1))
										? (++r, (t += 4))
										: (t += 3);
								return t;
							}),
								(r.read = function (e, t, n) {
									if (n - t < 1) return "";
									for (var r, i = null, o = [], s = 0; t < n; )
										(r = e[t++]) < 128
											? (o[s++] = r)
											: r > 191 && r < 224
											? (o[s++] = ((31 & r) << 6) | (63 & e[t++]))
											: r > 239 && r < 365
											? ((r =
													(((7 & r) << 18) |
														((63 & e[t++]) << 12) |
														((63 & e[t++]) << 6) |
														(63 & e[t++])) -
													65536),
											  (o[s++] = 55296 + (r >> 10)),
											  (o[s++] = 56320 + (1023 & r)))
											: (o[s++] =
													((15 & r) << 12) |
													((63 & e[t++]) << 6) |
													(63 & e[t++])),
											s > 8191 &&
												((i || (i = [])).push(
													String.fromCharCode.apply(String, o)
												),
												(s = 0));
									return i
										? (s &&
												i.push(
													String.fromCharCode.apply(String, o.slice(0, s))
												),
										  i.join(""))
										: String.fromCharCode.apply(String, o.slice(0, s));
								}),
								(r.write = function (e, t, n) {
									for (var r, i, o = n, s = 0; s < e.length; ++s)
										(r = e.charCodeAt(s)) < 128
											? (t[n++] = r)
											: r < 2048
											? ((t[n++] = (r >> 6) | 192), (t[n++] = (63 & r) | 128))
											: 55296 == (64512 & r) &&
											  56320 == (64512 & (i = e.charCodeAt(s + 1)))
											? ((r = 65536 + ((1023 & r) << 10) + (1023 & i)),
											  ++s,
											  (t[n++] = (r >> 18) | 240),
											  (t[n++] = ((r >> 12) & 63) | 128),
											  (t[n++] = ((r >> 6) & 63) | 128),
											  (t[n++] = (63 & r) | 128))
											: ((t[n++] = (r >> 12) | 224),
											  (t[n++] = ((r >> 6) & 63) | 128),
											  (t[n++] = (63 & r) | 128));
									return n - o;
								});
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e, t, n) {
								var r = n || 8192,
									i = r >>> 1,
									o = null,
									s = r;
								return function (n) {
									if (n < 1 || n > i) return e(n);
									s + n > r && ((o = e(r)), (s = 0));
									var a = t.call(o, s, (s += n));
									return 7 & s && (s = 1 + (7 | s)), a;
								};
							};
						},
						function (e, t, n) {
							"use strict";
							e.exports = i;
							var r = n(1);
							function i(e, t) {
								(this.lo = e >>> 0), (this.hi = t >>> 0);
							}
							var o = (i.zero = new i(0, 0));
							(o.toNumber = function () {
								return 0;
							}),
								(o.zzEncode = o.zzDecode =
									function () {
										return this;
									}),
								(o.length = function () {
									return 1;
								});
							var s = (i.zeroHash = "\0\0\0\0\0\0\0\0");
							(i.fromNumber = function (e) {
								if (0 === e) return o;
								var t = e < 0;
								t && (e = -e);
								var n = e >>> 0,
									r = ((e - n) / 4294967296) >>> 0;
								return (
									t &&
										((r = ~r >>> 0),
										(n = ~n >>> 0),
										++n > 4294967295 && ((n = 0), ++r > 4294967295 && (r = 0))),
									new i(n, r)
								);
							}),
								(i.from = function (e) {
									if ("number" == typeof e) return i.fromNumber(e);
									if (r.isString(e)) {
										if (!r.Long) return i.fromNumber(parseInt(e, 10));
										e = r.Long.fromString(e);
									}
									return e.low || e.high ? new i(e.low >>> 0, e.high >>> 0) : o;
								}),
								(i.prototype.toNumber = function (e) {
									if (!e && this.hi >>> 31) {
										var t = (1 + ~this.lo) >>> 0,
											n = ~this.hi >>> 0;
										return t || (n = (n + 1) >>> 0), -(t + 4294967296 * n);
									}
									return this.lo + 4294967296 * this.hi;
								}),
								(i.prototype.toLong = function (e) {
									return r.Long
										? new r.Long(0 | this.lo, 0 | this.hi, Boolean(e))
										: {
												low: 0 | this.lo,
												high: 0 | this.hi,
												unsigned: Boolean(e),
										  };
								});
							var a = String.prototype.charCodeAt;
							(i.fromHash = function (e) {
								return e === s
									? o
									: new i(
											(a.call(e, 0) |
												(a.call(e, 1) << 8) |
												(a.call(e, 2) << 16) |
												(a.call(e, 3) << 24)) >>>
												0,
											(a.call(e, 4) |
												(a.call(e, 5) << 8) |
												(a.call(e, 6) << 16) |
												(a.call(e, 7) << 24)) >>>
												0
									  );
							}),
								(i.prototype.toHash = function () {
									return String.fromCharCode(
										255 & this.lo,
										(this.lo >>> 8) & 255,
										(this.lo >>> 16) & 255,
										this.lo >>> 24,
										255 & this.hi,
										(this.hi >>> 8) & 255,
										(this.hi >>> 16) & 255,
										this.hi >>> 24
									);
								}),
								(i.prototype.zzEncode = function () {
									var e = this.hi >> 31;
									return (
										(this.hi = (((this.hi << 1) | (this.lo >>> 31)) ^ e) >>> 0),
										(this.lo = ((this.lo << 1) ^ e) >>> 0),
										this
									);
								}),
								(i.prototype.zzDecode = function () {
									var e = -(1 & this.lo);
									return (
										(this.lo = (((this.lo >>> 1) | (this.hi << 31)) ^ e) >>> 0),
										(this.hi = ((this.hi >>> 1) ^ e) >>> 0),
										this
									);
								}),
								(i.prototype.length = function () {
									var e = this.lo,
										t = ((this.lo >>> 28) | (this.hi << 4)) >>> 0,
										n = this.hi >>> 24;
									return 0 === n
										? 0 === t
											? e < 16384
												? e < 128
													? 1
													: 2
												: e < 2097152
												? 3
												: 4
											: t < 16384
											? t < 128
												? 5
												: 6
											: t < 2097152
											? 7
											: 8
										: n < 128
										? 9
										: 10;
								});
						},
						function (e, t, n) {
							"use strict";
							e.exports = o;
							var r = n(3);
							(o.prototype = Object.create(r.prototype)).constructor = o;
							var i = n(1);
							function o() {
								r.call(this);
							}
							function s(e, t, n) {
								e.length < 40
									? i.utf8.write(e, t, n)
									: t.utf8Write
									? t.utf8Write(e, n)
									: t.write(e, n);
							}
							(o._configure = function () {
								(o.alloc = i._Buffer_allocUnsafe),
									(o.writeBytesBuffer =
										i.Buffer &&
										i.Buffer.prototype instanceof Uint8Array &&
										"set" === i.Buffer.prototype.set.name
											? function (e, t, n) {
													t.set(e, n);
											  }
											: function (e, t, n) {
													if (e.copy) e.copy(t, n, 0, e.length);
													else for (var r = 0; r < e.length; ) t[n++] = e[r++];
											  });
							}),
								(o.prototype.bytes = function (e) {
									i.isString(e) && (e = i._Buffer_from(e, "base64"));
									var t = e.length >>> 0;
									return (
										this.uint32(t),
										t && this._push(o.writeBytesBuffer, t, e),
										this
									);
								}),
								(o.prototype.string = function (e) {
									var t = i.Buffer.byteLength(e);
									return this.uint32(t), t && this._push(s, t, e), this;
								}),
								o._configure();
						},
						function (e, t, n) {
							"use strict";
							e.exports = o;
							var r = n(4);
							(o.prototype = Object.create(r.prototype)).constructor = o;
							var i = n(1);
							function o(e) {
								r.call(this, e);
							}
							(o._configure = function () {
								i.Buffer && (o.prototype._slice = i.Buffer.prototype.slice);
							}),
								(o.prototype.string = function () {
									var e = this.uint32();
									return this.buf.utf8Slice
										? this.buf.utf8Slice(
												this.pos,
												(this.pos = Math.min(this.pos + e, this.len))
										  )
										: this.buf.toString(
												"utf-8",
												this.pos,
												(this.pos = Math.min(this.pos + e, this.len))
										  );
								}),
								o._configure();
						},
						function (e, t, n) {
							"use strict";
							t.Service = n(30);
						},
						function (e, t, n) {
							"use strict";
							e.exports = i;
							var r = n(1);
							function i(e, t, n) {
								if ("function" != typeof e)
									throw TypeError("rpcImpl must be a function");
								r.EventEmitter.call(this),
									(this.rpcImpl = e),
									(this.requestDelimited = Boolean(t)),
									(this.responseDelimited = Boolean(n));
							}
							((i.prototype = Object.create(
								r.EventEmitter.prototype
							)).constructor = i),
								(i.prototype.rpcCall = function e(t, n, i, o, s) {
									if (!o) throw TypeError("request must be specified");
									var a = this;
									if (!s) return r.asPromise(e, a, t, n, i, o);
									if (a.rpcImpl)
										try {
											return a.rpcImpl(
												t,
												n[a.requestDelimited ? "encodeDelimited" : "encode"](
													o
												).finish(),
												function (e, n) {
													if (e) return a.emit("error", e, t), s(e);
													if (null !== n) {
														if (!(n instanceof i))
															try {
																n =
																	i[
																		a.responseDelimited
																			? "decodeDelimited"
																			: "decode"
																	](n);
															} catch (e) {
																return a.emit("error", e, t), s(e);
															}
														return a.emit("data", n, t), s(null, n);
													}
													a.end(!0);
												}
											);
										} catch (e) {
											return (
												a.emit("error", e, t),
												void setTimeout(function () {
													s(e);
												}, 0)
											);
										}
									else
										setTimeout(function () {
											s(Error("already ended"));
										}, 0);
								}),
								(i.prototype.end = function (e) {
									return (
										this.rpcImpl &&
											(e || this.rpcImpl(null, null, null),
											(this.rpcImpl = null),
											this.emit("end").off()),
										this
									);
								});
						},
						function (e, t, n) {
							"use strict";
							e.exports = {};
						},
						function (e, t, n) {
							"use strict";
							Object.defineProperty(t, "__esModule", { value: !0 }),
								(t.verifyConfig = t.ConfigError = t.newStatsReporter = void 0);
							var r = n(33);
							Object.defineProperty(t, "newStatsReporter", {
								enumerable: !0,
								get: function () {
									return r.newStatsReporter;
								},
							});
							var i = n(14);
							Object.defineProperty(t, "ConfigError", {
								enumerable: !0,
								get: function () {
									return i.ConfigError;
								},
							}),
								Object.defineProperty(t, "verifyConfig", {
									enumerable: !0,
									get: function () {
										return i.verifyConfig;
									},
								}),
								(t.default = r.default);
						},
						function (e, t, n) {
							"use strict";
							var r =
								(this && this.__assign) ||
								function () {
									return (r =
										Object.assign ||
										function (e) {
											for (var t, n = 1, r = arguments.length; n < r; n++)
												for (var i in (t = arguments[n]))
													Object.prototype.hasOwnProperty.call(t, i) &&
														(e[i] = t[i]);
											return e;
										}).apply(this, arguments);
								};
							Object.defineProperty(t, "__esModule", { value: !0 }),
								(t.newStatsReporter = void 0);
							var i = n(2),
								o = n(5),
								s = n(52),
								a = n(14),
								u = function (e, t, n, r) {
									var o = e.get(r) || new i.PeerMetrics({ remotePid: r });
									return (
										(o.sizeBytes += t),
										(o.timespent += n),
										(o.cntChunks += 1),
										e.set(r, o),
										e
									);
								},
								c = function (e) {
									var t = [];
									return (
										e.forEach(function (e) {
											t.push(e);
										}),
										t
									);
								};
							function l() {
								try {
									if (
										localStorage &&
										localStorage.getItem &&
										localStorage.setItem
									)
										return localStorage;
								} catch (e) {}
								return {
									getItem: function (e) {
										return "unknown";
									},
									setItem: function (e, t) {},
								};
							}
							var f = (function () {
								function e() {
									(this.cumulatedData = s.createDefaultDataStats()),
										(this.qoeStats = s.createDefaultQoe()),
										(this.p2pStats = s.createDefaultP2PStats()),
										(this.playerStats = s.createDefautPlayerStats()),
										(this.deviceStats = s.createDefaultDeviceStats()),
										(this._countOffers = []),
										(this._internalPeerMetricsSeeder = new Map()),
										(this._internalPeerMetricsLeecher = new Map()),
										(this._internalDelayMap = new Map()),
										(this.currentCnt = 0),
										(this.lastSent = new Date());
								}
								return (
									(e.prototype.useConnector = function (e) {
										return (this.serverConnector = e), this;
									}),
									(e.prototype.setMediaMetadata = function (e) {
										this.mediaMetadata = e;
									}),
									(e.prototype.setAgentInfo = function (e) {
										console.log("avgNumOffer init", this.p2pStats.avgNumOffer),
											console.log("p2pStats init", this.p2pStats),
											(this.agentInfo = e);
									}),
									(e.prototype.reportQoE = function (e) {
										this.qoeStats = new i.QoEStats(
											r(
												r({}, this.qoeStats),
												Object.entries(e)
													.filter(function (e) {
														e[0];
														var t = e[1];
														return (
															(Array.isArray(t) && t.length > 0) ||
															(!Array.isArray(t) && !!t)
														);
													})
													.reduce(function (e, t) {
														var n;
														return r(r({}, e), (((n = {})[t[0]] = t[1]), n));
													}, {})
											)
										);
									}),
									(e.prototype.setInstantQoE = function (e) {
										(this.qoeStats.startupTime = e.startupTime),
											(this.qoeStats.bufferLength = e.bufferLength);
									}),
									(e.prototype.incrementQoE = function (e) {
										(this.qoeStats.rebufferCnt += e.rebufferCnt || 0),
											(this.qoeStats.rebufferTime += e.rebufferTime || 0),
											(this.qoeStats.switchUp += e.switchUp || 0),
											(this.qoeStats.switchDown += e.switchDown || 0),
											(this.qoeStats.watchingTime += e.watchingTime || 0);
									}),
									(e.prototype.setQualitySwitches = function (e, t) {
										(this.qoeStats.switchUp = e),
											(this.qoeStats.switchDown = t);
									}),
									(e.prototype.setQualityChunks = function (e) {
										this.qoeStats = new i.QoEStats(
											r(r({}, this.qoeStats), { qualityChkCnt: Array.from(e) })
										);
									}),
									(e.prototype.incrementPlayerEvents = function (e) {
										this.playerStats[e] += 1;
									}),
									(e.prototype.reportDelay = function (e, t) {
										var n =
											this._internalDelayMap.get(e) ||
											new i.PeerDelay({
												remotePid: e,
												avgDelay: 0,
												cntPpmsg: 0,
											});
										(n.avgDelay =
											(n.avgDelay * n.cntPpmsg + t) / (n.cntPpmsg + 1)),
											(n.cntPpmsg += 1),
											this._internalDelayMap.set(e, n);
									}),
									(e.prototype.reportResourceAvailability = function (e, t) {
										var n = this;
										console.log("reportResourceAvailability", e),
											console.log(
												"avgNumOffer before",
												this.p2pStats.avgNumOffer
											),
											e.forEach(function (e) {
												n._internalPeerMetricsSeeder = (function (e, t) {
													if (e.has(t)) {
														var n = e.get(t);
														(n.cntHasChunks += 1), e.set(t, n);
													}
													return e;
												})(n._internalPeerMetricsSeeder, e);
											}),
											(this.p2pStats.cntActiveChunks += 1),
											this._countOffers.push(e.length),
											(this.p2pStats.stdNumOffer = (function (e) {
												var t = e.length;
												if (0 === t) return null;
												var n =
													e.reduce(function (e, t) {
														return e + t;
													}, 0) / t;
												return Math.sqrt(
													e
														.map(function (e) {
															return Math.pow(e - n, 2);
														})
														.reduce(function (e, t) {
															return e + t;
														}) / t
												);
											})(this._countOffers)),
											(this.p2pStats.avgNumOffer =
												(e.length +
													this.p2pStats.avgNumOffer *
														(this._countOffers.length - 1)) /
												this._countOffers.length),
											console.log(
												"avgNumOffer after",
												this.p2pStats.avgNumOffer
											);
									}),
									(e.prototype.incrementP2PEvents = function (e) {
										switch (e) {
											case "connected":
												this.p2pStats.cntConnected += 1;
												break;
											case "connect_err":
												this.p2pStats.cntConnectErr += 1;
												break;
											case "disconnect":
												this.p2pStats.cntDisconnect += 1;
												break;
											case "chn_switch":
												this.p2pStats.cntChnSwitch += 1;
												break;
											case "pingpong":
												this.p2pStats.cntDisconnectPp += 1;
										}
									}),
									(e.prototype.reportExchange = function (e, t, n, r) {
										if (e < 0 || t < 0)
											throw RangeError(
												"The size bytes and timespent should not be less than 0"
											);
										switch (((this.currentCnt += 1), n)) {
											case "cdn":
												(this.cumulatedData.bytesCdn += e),
													(this.cumulatedData.cntCdn += 1),
													(this.cumulatedData.timespentCdn += t);
												break;
											case "p2p":
												if (!r)
													throw Error(
														"The exchanged peer is needed for p2p resources"
													);
												(this._internalPeerMetricsSeeder = u(
													this._internalPeerMetricsSeeder,
													e,
													t,
													r
												)),
													(this.cumulatedData.bytesP2p += e),
													(this.cumulatedData.cntP2p += 1),
													(this.cumulatedData.timespentP2p += t);
												break;
											case "p2p_upload":
												if (!r)
													throw Error(
														"The exchanged peer is needed for p2p resources"
													);
												(this._internalPeerMetricsLeecher = u(
													this._internalPeerMetricsLeecher,
													e,
													t,
													r
												)),
													(this.cumulatedData.bytesP2pUpload += e),
													(this.cumulatedData.cntP2pUpload += 1),
													(this.cumulatedData.timespentP2pUpload += t);
										}
										(this.p2pStats.leechers = c(
											this._internalPeerMetricsLeecher
										)),
											(this.p2pStats.seeders = c(
												this._internalPeerMetricsSeeder
											)),
											(this.p2pStats.delays = Array.from(
												this._internalDelayMap.values()
											)),
											(this.p2pStats.cntSeeders = this.p2pStats.seeders.length),
											(this.p2pStats.cntLeechers =
												this.p2pStats.leechers.length);
									}),
									(e.prototype.reportDeviceStats = function (e, t, n) {
										this.deviceStats = new i.DeviceStats({
											batteryLevel: e,
											totalMemory: t,
											usedMemory: n,
										});
									}),
									(e.prototype.isValidStats = function (e) {
										return !(
											!e ||
											!e.agent ||
											!(
												(e.agent && "" !== e.agent.contentId) ||
												(e.mediaMeta && "" !== e.mediaMeta.url)
											) ||
											!e.data ||
											e.data.cntCdn > 100 ||
											e.data.cntP2p > 100 ||
											0 === Object.keys(e.data).length
										);
									}),
									(e.prototype.restartReportLoop = function (e) {
										var t = this;
										this.intervalId && clearInterval(this.intervalId),
											(this.intervalId = setInterval(function () {
												var e = t.snapshotCurrentState();
												t.isValidStats(e)
													? t.serverConnector
															.sendStats(e)
															.then(function (e) {
																var n,
																	r = null == e ? void 0 : e.data;
																null === (n = l()) ||
																	void 0 === n ||
																	n.setItem(
																		"user_id",
																		null == r ? void 0 : r.u
																	),
																	(t.agentInfo.userId =
																		null == r ? void 0 : r.u);
															})
															.catch(function (e) {
																console.warn(e);
															})
															.finally(function () {
																t.cleanCurrentStats();
															})
													: t.cleanCurrentStats();
											}, e));
									}),
									(e.prototype.stopReportLoop = function () {
										this.intervalId && clearInterval(this.intervalId);
									}),
									(e.prototype.snapshotCurrentState = function () {
										var e =
											(new Date().getTime() - this.lastSent.getTime()) / 1e3;
										return new i.Stats({
											agent: r({}, this.agentInfo),
											ts: new Date().getTime(),
											data: r({}, this.cumulatedData),
											qoe: r(r({}, this.qoeStats), { watchingTime: e }),
											p2p: r({}, this.p2pStats),
											mediaMeta: r({}, this.mediaMetadata),
											player: r({}, this.playerStats),
											device: r({}, this.deviceStats),
										});
									}),
									(e.prototype.cleanCurrentStats = function () {
										(this.currentCnt = 0),
											(this.cumulatedData = new i.DataStats()),
											(this.lastSent = new Date()),
											this._internalPeerMetricsLeecher.clear(),
											this._internalPeerMetricsSeeder.clear(),
											this._internalDelayMap.clear(),
											(this._countOffers = []),
											(this.p2pStats = s.createDefaultP2PStats()),
											(this.qoeStats = s.createDefaultQoe()),
											(this.playerStats = s.createDefautPlayerStats()),
											(this.deviceStats = s.createDefaultDeviceStats());
									}),
									e
								);
							})();
							(t.newStatsReporter = function (
								e,
								t,
								n,
								r,
								s,
								u,
								c,
								p,
								h,
								g,
								d,
								y
							) {
								return (
									y ||
										null === l().getItem("user_id") ||
										(y = l().getItem("user_id")),
									(function (e) {
										a.verifyConfig(e);
										var t = new f();
										return (
											t.setAgentInfo(e.agentInfo),
											t.setMediaMetadata(e.mediaMetadata),
											t.useConnector(o.newStatsServerConnector(e.url)),
											t
										);
									})({
										url: e,
										mediaMetadata: new i.MediaMetadata({
											url: t,
											videoFormat: n,
											vod: r,
										}),
										agentInfo: new i.AgentInfo({
											apiKey: s,
											pid: u,
											origin: h,
											contentId: c,
											version: p,
											userAgent: g,
											ip: d,
											userId: y,
										}),
									})
								);
							}),
								(t.default = f);
						},
						function (e, t, n) {
							e.exports = n(35);
						},
						function (e, t, n) {
							"use strict";
							var r = n(0),
								i = n(6),
								o = n(36),
								s = n(12);
							function a(e) {
								var t = new o(e),
									n = i(o.prototype.request, t);
								return r.extend(n, o.prototype, t), r.extend(n, t), n;
							}
							var u = a(n(9));
							(u.Axios = o),
								(u.create = function (e) {
									return a(s(u.defaults, e));
								}),
								(u.Cancel = n(13)),
								(u.CancelToken = n(50)),
								(u.isCancel = n(8)),
								(u.all = function (e) {
									return Promise.all(e);
								}),
								(u.spread = n(51)),
								(e.exports = u),
								(e.exports.default = u);
						},
						function (e, t, n) {
							"use strict";
							var r = n(0),
								i = n(7),
								o = n(37),
								s = n(38),
								a = n(12);
							function u(e) {
								(this.defaults = e),
									(this.interceptors = { request: new o(), response: new o() });
							}
							(u.prototype.request = function (e) {
								"string" == typeof e
									? ((e = arguments[1] || {}).url = arguments[0])
									: (e = e || {}),
									(e = a(this.defaults, e)).method
										? (e.method = e.method.toLowerCase())
										: this.defaults.method
										? (e.method = this.defaults.method.toLowerCase())
										: (e.method = "get");
								var t = [s, void 0],
									n = Promise.resolve(e);
								for (
									this.interceptors.request.forEach(function (e) {
										t.unshift(e.fulfilled, e.rejected);
									}),
										this.interceptors.response.forEach(function (e) {
											t.push(e.fulfilled, e.rejected);
										});
									t.length;

								)
									n = n.then(t.shift(), t.shift());
								return n;
							}),
								(u.prototype.getUri = function (e) {
									return (
										(e = a(this.defaults, e)),
										i(e.url, e.params, e.paramsSerializer).replace(/^\?/, "")
									);
								}),
								r.forEach(["delete", "get", "head", "options"], function (e) {
									u.prototype[e] = function (t, n) {
										return this.request(a(n || {}, { method: e, url: t }));
									};
								}),
								r.forEach(["post", "put", "patch"], function (e) {
									u.prototype[e] = function (t, n, r) {
										return this.request(
											a(r || {}, { method: e, url: t, data: n })
										);
									};
								}),
								(e.exports = u);
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							function i() {
								this.handlers = [];
							}
							(i.prototype.use = function (e, t) {
								return (
									this.handlers.push({ fulfilled: e, rejected: t }),
									this.handlers.length - 1
								);
							}),
								(i.prototype.eject = function (e) {
									this.handlers[e] && (this.handlers[e] = null);
								}),
								(i.prototype.forEach = function (e) {
									r.forEach(this.handlers, function (t) {
										null !== t && e(t);
									});
								}),
								(e.exports = i);
						},
						function (e, t, n) {
							"use strict";
							var r = n(0),
								i = n(39),
								o = n(8),
								s = n(9);
							function a(e) {
								e.cancelToken && e.cancelToken.throwIfRequested();
							}
							e.exports = function (e) {
								return (
									a(e),
									(e.headers = e.headers || {}),
									(e.data = i(e.data, e.headers, e.transformRequest)),
									(e.headers = r.merge(
										e.headers.common || {},
										e.headers[e.method] || {},
										e.headers
									)),
									r.forEach(
										["delete", "get", "head", "post", "put", "patch", "common"],
										function (t) {
											delete e.headers[t];
										}
									),
									(e.adapter || s.adapter)(e).then(
										function (t) {
											return (
												a(e),
												(t.data = i(t.data, t.headers, e.transformResponse)),
												t
											);
										},
										function (t) {
											return (
												o(t) ||
													(a(e),
													t &&
														t.response &&
														(t.response.data = i(
															t.response.data,
															t.response.headers,
															e.transformResponse
														))),
												Promise.reject(t)
											);
										}
									)
								);
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							e.exports = function (e, t, n) {
								return (
									r.forEach(n, function (n) {
										e = n(e, t);
									}),
									e
								);
							};
						},
						function (e, t) {
							var n,
								r,
								i = (e.exports = {});
							function o() {
								throw new Error("setTimeout has not been defined");
							}
							function s() {
								throw new Error("clearTimeout has not been defined");
							}
							function a(e) {
								if (n === setTimeout) return setTimeout(e, 0);
								if ((n === o || !n) && setTimeout)
									return (n = setTimeout), setTimeout(e, 0);
								try {
									return n(e, 0);
								} catch (t) {
									try {
										return n.call(null, e, 0);
									} catch (t) {
										return n.call(this, e, 0);
									}
								}
							}
							!(function () {
								try {
									n = "function" == typeof setTimeout ? setTimeout : o;
								} catch (e) {
									n = o;
								}
								try {
									r = "function" == typeof clearTimeout ? clearTimeout : s;
								} catch (e) {
									r = s;
								}
							})();
							var u,
								c = [],
								l = !1,
								f = -1;
							function p() {
								l &&
									u &&
									((l = !1),
									u.length ? (c = u.concat(c)) : (f = -1),
									c.length && h());
							}
							function h() {
								if (!l) {
									var e = a(p);
									l = !0;
									for (var t = c.length; t; ) {
										for (u = c, c = []; ++f < t; ) u && u[f].run();
										(f = -1), (t = c.length);
									}
									(u = null),
										(l = !1),
										(function (e) {
											if (r === clearTimeout) return clearTimeout(e);
											if ((r === s || !r) && clearTimeout)
												return (r = clearTimeout), clearTimeout(e);
											try {
												r(e);
											} catch (t) {
												try {
													return r.call(null, e);
												} catch (t) {
													return r.call(this, e);
												}
											}
										})(e);
								}
							}
							function g(e, t) {
								(this.fun = e), (this.array = t);
							}
							function d() {}
							(i.nextTick = function (e) {
								var t = new Array(arguments.length - 1);
								if (arguments.length > 1)
									for (var n = 1; n < arguments.length; n++)
										t[n - 1] = arguments[n];
								c.push(new g(e, t)), 1 !== c.length || l || a(h);
							}),
								(g.prototype.run = function () {
									this.fun.apply(null, this.array);
								}),
								(i.title = "browser"),
								(i.browser = !0),
								(i.env = {}),
								(i.argv = []),
								(i.version = ""),
								(i.versions = {}),
								(i.on = d),
								(i.addListener = d),
								(i.once = d),
								(i.off = d),
								(i.removeListener = d),
								(i.removeAllListeners = d),
								(i.emit = d),
								(i.prependListener = d),
								(i.prependOnceListener = d),
								(i.listeners = function (e) {
									return [];
								}),
								(i.binding = function (e) {
									throw new Error("process.binding is not supported");
								}),
								(i.cwd = function () {
									return "/";
								}),
								(i.chdir = function (e) {
									throw new Error("process.chdir is not supported");
								}),
								(i.umask = function () {
									return 0;
								});
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							e.exports = function (e, t) {
								r.forEach(e, function (n, r) {
									r !== t &&
										r.toUpperCase() === t.toUpperCase() &&
										((e[t] = n), delete e[r]);
								});
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(11);
							e.exports = function (e, t, n) {
								var i = n.config.validateStatus;
								n.status && i && !i(n.status)
									? t(
											r(
												"Request failed with status code " + n.status,
												n.config,
												null,
												n.request,
												n
											)
									  )
									: e(n);
							};
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e, t, n, r, i) {
								return (
									(e.config = t),
									n && (e.code = n),
									(e.request = r),
									(e.response = i),
									(e.isAxiosError = !0),
									(e.toJSON = function () {
										return {
											message: this.message,
											name: this.name,
											description: this.description,
											number: this.number,
											fileName: this.fileName,
											lineNumber: this.lineNumber,
											columnNumber: this.columnNumber,
											stack: this.stack,
											config: this.config,
											code: this.code,
										};
									}),
									e
								);
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							e.exports = r.isStandardBrowserEnv()
								? {
										write: function (e, t, n, i, o, s) {
											var a = [];
											a.push(e + "=" + encodeURIComponent(t)),
												r.isNumber(n) &&
													a.push("expires=" + new Date(n).toGMTString()),
												r.isString(i) && a.push("path=" + i),
												r.isString(o) && a.push("domain=" + o),
												!0 === s && a.push("secure"),
												(document.cookie = a.join("; "));
										},
										read: function (e) {
											var t = document.cookie.match(
												new RegExp("(^|;\\s*)(" + e + ")=([^;]*)")
											);
											return t ? decodeURIComponent(t[3]) : null;
										},
										remove: function (e) {
											this.write(e, "", Date.now() - 864e5);
										},
								  }
								: {
										write: function () {},
										read: function () {
											return null;
										},
										remove: function () {},
								  };
						},
						function (e, t, n) {
							"use strict";
							var r = n(46),
								i = n(47);
							e.exports = function (e, t) {
								return e && !r(t) ? i(e, t) : t;
							};
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e) {
								return /^([a-z][a-z\d\+\-\.]*:)?\/\//i.test(e);
							};
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e, t) {
								return t
									? e.replace(/\/+$/, "") + "/" + t.replace(/^\/+/, "")
									: e;
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(0),
								i = [
									"age",
									"authorization",
									"content-length",
									"content-type",
									"etag",
									"expires",
									"from",
									"host",
									"if-modified-since",
									"if-unmodified-since",
									"last-modified",
									"location",
									"max-forwards",
									"proxy-authorization",
									"referer",
									"retry-after",
									"user-agent",
								];
							e.exports = function (e) {
								var t,
									n,
									o,
									s = {};
								return e
									? (r.forEach(e.split("\n"), function (e) {
											if (
												((o = e.indexOf(":")),
												(t = r.trim(e.substr(0, o)).toLowerCase()),
												(n = r.trim(e.substr(o + 1))),
												t)
											) {
												if (s[t] && i.indexOf(t) >= 0) return;
												s[t] =
													"set-cookie" === t
														? (s[t] ? s[t] : []).concat([n])
														: s[t]
														? s[t] + ", " + n
														: n;
											}
									  }),
									  s)
									: s;
							};
						},
						function (e, t, n) {
							"use strict";
							var r = n(0);
							e.exports = r.isStandardBrowserEnv()
								? (function () {
										var e,
											t = /(msie|trident)/i.test(navigator.userAgent),
											n = document.createElement("a");
										function i(e) {
											var r = e;
											return (
												t && (n.setAttribute("href", r), (r = n.href)),
												n.setAttribute("href", r),
												{
													href: n.href,
													protocol: n.protocol
														? n.protocol.replace(/:$/, "")
														: "",
													host: n.host,
													search: n.search ? n.search.replace(/^\?/, "") : "",
													hash: n.hash ? n.hash.replace(/^#/, "") : "",
													hostname: n.hostname,
													port: n.port,
													pathname:
														"/" === n.pathname.charAt(0)
															? n.pathname
															: "/" + n.pathname,
												}
											);
										}
										return (
											(e = i(window.location.href)),
											function (t) {
												var n = r.isString(t) ? i(t) : t;
												return n.protocol === e.protocol && n.host === e.host;
											}
										);
								  })()
								: function () {
										return !0;
								  };
						},
						function (e, t, n) {
							"use strict";
							var r = n(13);
							function i(e) {
								if ("function" != typeof e)
									throw new TypeError("executor must be a function.");
								var t;
								this.promise = new Promise(function (e) {
									t = e;
								});
								var n = this;
								e(function (e) {
									n.reason || ((n.reason = new r(e)), t(n.reason));
								});
							}
							(i.prototype.throwIfRequested = function () {
								if (this.reason) throw this.reason;
							}),
								(i.source = function () {
									var e;
									return {
										token: new i(function (t) {
											e = t;
										}),
										cancel: e,
									};
								}),
								(e.exports = i);
						},
						function (e, t, n) {
							"use strict";
							e.exports = function (e) {
								return function (t) {
									return e.apply(null, t);
								};
							};
						},
						function (e, t, n) {
							"use strict";
							Object.defineProperty(t, "__esModule", { value: !0 }),
								(t.createDefaultDeviceStats =
									t.createDefautPlayerStats =
									t.createDefaultQoe =
									t.createDefaultP2PStats =
									t.createDefaultDataStats =
										void 0);
							var r = n(2);
							(t.createDefaultDataStats = function () {
								return new r.DataStats({});
							}),
								(t.createDefaultP2PStats = function () {
									return new r.P2PStats({
										cntLeechers: 0,
										cntSeeders: 0,
										leechers: [],
										seeders: [],
										delays: [],
										cntActiveChunks: 0,
										cntConnected: 0,
										cntConnectErr: 0,
										cntDisconnect: 0,
										cntChnSwitch: 0,
										cntDisconnectPp: 0,
									});
								}),
								(t.createDefaultQoe = function () {
									return new r.QoEStats({
										rebufferTime: 0,
										rebufferCnt: 0,
										qualityChkCnt: [],
										switchDown: 0,
										switchUp: 0,
									});
								}),
								(t.createDefautPlayerStats = function () {
									return new r.PlayerStats({
										cntPlay: 0,
										cntPause: 0,
										cntNext: 0,
										cntPrev: 0,
										cntMqc: 0,
										cntPip: 0,
										cntSeek: 0,
										cntLc: 0,
										cntSc: 0,
									});
								}),
								(t.createDefaultDeviceStats = function () {
									return new r.DeviceStats({
										batteryLevel: 0,
										totalMemory: 0,
										usedMemory: 0,
									});
								});
						},
					]);
				}),
				(module.exports = e());
		},
		function (e, t, n) {
			"use strict";
			var r,
				i =
					(this && this.__extends) ||
					((r = function (e, t) {
						return (r =
							Object.setPrototypeOf ||
							({ __proto__: [] } instanceof Array &&
								function (e, t) {
									e.__proto__ = t;
								}) ||
							function (e, t) {
								for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
							})(e, t);
					}),
					function (e, t) {
						function n() {
							this.constructor = e;
						}
						r(e, t),
							(e.prototype =
								null === t
									? Object.create(t)
									: ((n.prototype = t.prototype), new n()));
					});
			Object.defineProperty(t, "__esModule", { value: !0 });
			var o = n(20),
				s = n(21),
				a = n(14),
				u = n(15),
				c = n(13),
				l = n(22),
				f = (function (e) {
					function t(n, r, i) {
						var o = e.call(this) || this;
						switch (
							((o.syncErrorValue = null),
							(o.syncErrorThrown = !1),
							(o.syncErrorThrowable = !1),
							(o.isStopped = !1),
							arguments.length)
						) {
							case 0:
								o.destination = s.empty;
								break;
							case 1:
								if (!n) {
									o.destination = s.empty;
									break;
								}
								if ("object" == typeof n) {
									n instanceof t
										? ((o.syncErrorThrowable = n.syncErrorThrowable),
										  (o.destination = n),
										  n.add(o))
										: ((o.syncErrorThrowable = !0),
										  (o.destination = new p(o, n)));
									break;
								}
							default:
								(o.syncErrorThrowable = !0),
									(o.destination = new p(o, n, r, i));
						}
						return o;
					}
					return (
						i(t, e),
						(t.prototype[u.rxSubscriber] = function () {
							return this;
						}),
						(t.create = function (e, n, r) {
							var i = new t(e, n, r);
							return (i.syncErrorThrowable = !1), i;
						}),
						(t.prototype.next = function (e) {
							this.isStopped || this._next(e);
						}),
						(t.prototype.error = function (e) {
							this.isStopped || ((this.isStopped = !0), this._error(e));
						}),
						(t.prototype.complete = function () {
							this.isStopped || ((this.isStopped = !0), this._complete());
						}),
						(t.prototype.unsubscribe = function () {
							this.closed ||
								((this.isStopped = !0), e.prototype.unsubscribe.call(this));
						}),
						(t.prototype._next = function (e) {
							this.destination.next(e);
						}),
						(t.prototype._error = function (e) {
							this.destination.error(e), this.unsubscribe();
						}),
						(t.prototype._complete = function () {
							this.destination.complete(), this.unsubscribe();
						}),
						(t.prototype._unsubscribeAndRecycle = function () {
							var e = this._parentOrParents;
							return (
								(this._parentOrParents = null),
								this.unsubscribe(),
								(this.closed = !1),
								(this.isStopped = !1),
								(this._parentOrParents = e),
								this
							);
						}),
						t
					);
				})(a.Subscription);
			t.Subscriber = f;
			var p = (function (e) {
				function t(t, n, r, i) {
					var a,
						u = e.call(this) || this;
					u._parentSubscriber = t;
					var c = u;
					return (
						o.isFunction(n)
							? (a = n)
							: n &&
							  ((a = n.next),
							  (r = n.error),
							  (i = n.complete),
							  n !== s.empty &&
									((c = Object.create(n)),
									o.isFunction(c.unsubscribe) && u.add(c.unsubscribe.bind(c)),
									(c.unsubscribe = u.unsubscribe.bind(u)))),
						(u._context = c),
						(u._next = a),
						(u._error = r),
						(u._complete = i),
						u
					);
				}
				return (
					i(t, e),
					(t.prototype.next = function (e) {
						if (!this.isStopped && this._next) {
							var t = this._parentSubscriber;
							c.config.useDeprecatedSynchronousErrorHandling &&
							t.syncErrorThrowable
								? this.__tryOrSetError(t, this._next, e) && this.unsubscribe()
								: this.__tryOrUnsub(this._next, e);
						}
					}),
					(t.prototype.error = function (e) {
						if (!this.isStopped) {
							var t = this._parentSubscriber,
								n = c.config.useDeprecatedSynchronousErrorHandling;
							if (this._error)
								n && t.syncErrorThrowable
									? (this.__tryOrSetError(t, this._error, e),
									  this.unsubscribe())
									: (this.__tryOrUnsub(this._error, e), this.unsubscribe());
							else if (t.syncErrorThrowable)
								n
									? ((t.syncErrorValue = e), (t.syncErrorThrown = !0))
									: l.hostReportError(e),
									this.unsubscribe();
							else {
								if ((this.unsubscribe(), n)) throw e;
								l.hostReportError(e);
							}
						}
					}),
					(t.prototype.complete = function () {
						var e = this;
						if (!this.isStopped) {
							var t = this._parentSubscriber;
							if (this._complete) {
								var n = function () {
									return e._complete.call(e._context);
								};
								c.config.useDeprecatedSynchronousErrorHandling &&
								t.syncErrorThrowable
									? (this.__tryOrSetError(t, n), this.unsubscribe())
									: (this.__tryOrUnsub(n), this.unsubscribe());
							} else this.unsubscribe();
						}
					}),
					(t.prototype.__tryOrUnsub = function (e, t) {
						try {
							e.call(this._context, t);
						} catch (e) {
							if (
								(this.unsubscribe(),
								c.config.useDeprecatedSynchronousErrorHandling)
							)
								throw e;
							l.hostReportError(e);
						}
					}),
					(t.prototype.__tryOrSetError = function (e, t, n) {
						if (!c.config.useDeprecatedSynchronousErrorHandling)
							throw new Error("bad call");
						try {
							t.call(this._context, n);
						} catch (t) {
							return c.config.useDeprecatedSynchronousErrorHandling
								? ((e.syncErrorValue = t), (e.syncErrorThrown = !0), !0)
								: (l.hostReportError(t), !0);
						}
						return !1;
					}),
					(t.prototype._unsubscribe = function () {
						var e = this._parentSubscriber;
						(this._context = null),
							(this._parentSubscriber = null),
							e.unsubscribe();
					}),
					t
				);
			})(f);
			t.SafeSubscriber = p;
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = !1;
			t.config = {
				Promise: void 0,
				set useDeprecatedSynchronousErrorHandling(e) {
					if (e) {
						var t = new Error();
						console.warn(
							"DEPRECATED! RxJS was set to use deprecated synchronous error handling behavior by code at: \n" +
								t.stack
						);
					} else
						r &&
							console.log(
								"RxJS: Back to a better error behavior. Thank you. <3"
							);
					r = e;
				},
				get useDeprecatedSynchronousErrorHandling() {
					return r;
				},
			};
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = n(46),
				i = n(47),
				o = n(20),
				s = n(48),
				a = (function () {
					function e(e) {
						(this.closed = !1),
							(this._parentOrParents = null),
							(this._subscriptions = null),
							e && ((this._ctorUnsubscribe = !0), (this._unsubscribe = e));
					}
					var t;
					return (
						(e.prototype.unsubscribe = function () {
							var t;
							if (!this.closed) {
								var n = this._parentOrParents,
									a = this._ctorUnsubscribe,
									c = this._unsubscribe,
									l = this._subscriptions;
								if (
									((this.closed = !0),
									(this._parentOrParents = null),
									(this._subscriptions = null),
									n instanceof e)
								)
									n.remove(this);
								else if (null !== n)
									for (var f = 0; f < n.length; ++f) {
										n[f].remove(this);
									}
								if (o.isFunction(c)) {
									a && (this._unsubscribe = void 0);
									try {
										c.call(this);
									} catch (e) {
										t = e instanceof s.UnsubscriptionError ? u(e.errors) : [e];
									}
								}
								if (r.isArray(l)) {
									f = -1;
									for (var p = l.length; ++f < p; ) {
										var h = l[f];
										if (i.isObject(h))
											try {
												h.unsubscribe();
											} catch (e) {
												(t = t || []),
													e instanceof s.UnsubscriptionError
														? (t = t.concat(u(e.errors)))
														: t.push(e);
											}
									}
								}
								if (t) throw new s.UnsubscriptionError(t);
							}
						}),
						(e.prototype.add = function (t) {
							var n = t;
							if (!t) return e.EMPTY;
							switch (typeof t) {
								case "function":
									n = new e(t);
								case "object":
									if (
										n === this ||
										n.closed ||
										"function" != typeof n.unsubscribe
									)
										return n;
									if (this.closed) return n.unsubscribe(), n;
									if (!(n instanceof e)) {
										var r = n;
										(n = new e())._subscriptions = [r];
									}
									break;
								default:
									throw new Error(
										"unrecognized teardown " + t + " added to Subscription."
									);
							}
							var i = n._parentOrParents;
							if (null === i) n._parentOrParents = this;
							else if (i instanceof e) {
								if (i === this) return n;
								n._parentOrParents = [i, this];
							} else {
								if (-1 !== i.indexOf(this)) return n;
								i.push(this);
							}
							var o = this._subscriptions;
							return null === o ? (this._subscriptions = [n]) : o.push(n), n;
						}),
						(e.prototype.remove = function (e) {
							var t = this._subscriptions;
							if (t) {
								var n = t.indexOf(e);
								-1 !== n && t.splice(n, 1);
							}
						}),
						(e.EMPTY = (((t = new e()).closed = !0), t)),
						e
					);
				})();
			function u(e) {
				return e.reduce(function (e, t) {
					return e.concat(t instanceof s.UnsubscriptionError ? t.errors : t);
				}, []);
			}
			t.Subscription = a;
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.rxSubscriber =
					"function" == typeof Symbol
						? Symbol("rxSubscriber")
						: "@@rxSubscriber_" + Math.random()),
				(t.$$rxSubscriber = t.rxSubscriber);
		},
		function (e, t, n) {
			"use strict";
			var r,
				i =
					(this && this.__extends) ||
					((r = function (e, t) {
						return (r =
							Object.setPrototypeOf ||
							({ __proto__: [] } instanceof Array &&
								function (e, t) {
									e.__proto__ = t;
								}) ||
							function (e, t) {
								for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
							})(e, t);
					}),
					function (e, t) {
						function n() {
							this.constructor = e;
						}
						r(e, t),
							(e.prototype =
								null === t
									? Object.create(t)
									: ((n.prototype = t.prototype), new n()));
					});
			Object.defineProperty(t, "__esModule", { value: !0 });
			var o = n(8),
				s = n(12),
				a = n(14),
				u = n(53),
				c = n(54),
				l = n(15),
				f = (function (e) {
					function t(t) {
						var n = e.call(this, t) || this;
						return (n.destination = t), n;
					}
					return i(t, e), t;
				})(s.Subscriber);
			t.SubjectSubscriber = f;
			var p = (function (e) {
				function t() {
					var t = e.call(this) || this;
					return (
						(t.observers = []),
						(t.closed = !1),
						(t.isStopped = !1),
						(t.hasError = !1),
						(t.thrownError = null),
						t
					);
				}
				return (
					i(t, e),
					(t.prototype[l.rxSubscriber] = function () {
						return new f(this);
					}),
					(t.prototype.lift = function (e) {
						var t = new h(this, this);
						return (t.operator = e), t;
					}),
					(t.prototype.next = function (e) {
						if (this.closed) throw new u.ObjectUnsubscribedError();
						if (!this.isStopped)
							for (
								var t = this.observers, n = t.length, r = t.slice(), i = 0;
								i < n;
								i++
							)
								r[i].next(e);
					}),
					(t.prototype.error = function (e) {
						if (this.closed) throw new u.ObjectUnsubscribedError();
						(this.hasError = !0), (this.thrownError = e), (this.isStopped = !0);
						for (
							var t = this.observers, n = t.length, r = t.slice(), i = 0;
							i < n;
							i++
						)
							r[i].error(e);
						this.observers.length = 0;
					}),
					(t.prototype.complete = function () {
						if (this.closed) throw new u.ObjectUnsubscribedError();
						this.isStopped = !0;
						for (
							var e = this.observers, t = e.length, n = e.slice(), r = 0;
							r < t;
							r++
						)
							n[r].complete();
						this.observers.length = 0;
					}),
					(t.prototype.unsubscribe = function () {
						(this.isStopped = !0), (this.closed = !0), (this.observers = null);
					}),
					(t.prototype._trySubscribe = function (t) {
						if (this.closed) throw new u.ObjectUnsubscribedError();
						return e.prototype._trySubscribe.call(this, t);
					}),
					(t.prototype._subscribe = function (e) {
						if (this.closed) throw new u.ObjectUnsubscribedError();
						return this.hasError
							? (e.error(this.thrownError), a.Subscription.EMPTY)
							: this.isStopped
							? (e.complete(), a.Subscription.EMPTY)
							: (this.observers.push(e), new c.SubjectSubscription(this, e));
					}),
					(t.prototype.asObservable = function () {
						var e = new o.Observable();
						return (e.source = this), e;
					}),
					(t.create = function (e, t) {
						return new h(e, t);
					}),
					t
				);
			})(o.Observable);
			t.Subject = p;
			var h = (function (e) {
				function t(t, n) {
					var r = e.call(this) || this;
					return (r.destination = t), (r.source = n), r;
				}
				return (
					i(t, e),
					(t.prototype.next = function (e) {
						var t = this.destination;
						t && t.next && t.next(e);
					}),
					(t.prototype.error = function (e) {
						var t = this.destination;
						t && t.error && this.destination.error(e);
					}),
					(t.prototype.complete = function () {
						var e = this.destination;
						e && e.complete && this.destination.complete();
					}),
					(t.prototype._subscribe = function (e) {
						return this.source
							? this.source.subscribe(e)
							: a.Subscription.EMPTY;
					}),
					t
				);
			})(p);
			t.AnonymousSubject = h;
		},
		function (e, t, n) {
			"use strict";
			e.exports = n(25);
		},
		function (e, t, n) {
			"use strict";
			e.exports = f;
			var r,
				i = n(7),
				o = i.LongBits,
				s = i.base64,
				a = i.utf8;
			function u(e, t, n) {
				(this.fn = e), (this.len = t), (this.next = void 0), (this.val = n);
			}
			function c() {}
			function l(e) {
				(this.head = e.head),
					(this.tail = e.tail),
					(this.len = e.len),
					(this.next = e.states);
			}
			function f() {
				(this.len = 0),
					(this.head = new u(c, 0, 0)),
					(this.tail = this.head),
					(this.states = null);
			}
			var p = function () {
				return i.Buffer
					? function () {
							return (f.create = function () {
								return new r();
							})();
					  }
					: function () {
							return new f();
					  };
			};
			function h(e, t, n) {
				t[n] = 255 & e;
			}
			function g(e, t) {
				(this.len = e), (this.next = void 0), (this.val = t);
			}
			function d(e, t, n) {
				for (; e.hi; )
					(t[n++] = (127 & e.lo) | 128),
						(e.lo = ((e.lo >>> 7) | (e.hi << 25)) >>> 0),
						(e.hi >>>= 7);
				for (; e.lo > 127; ) (t[n++] = (127 & e.lo) | 128), (e.lo = e.lo >>> 7);
				t[n++] = e.lo;
			}
			function y(e, t, n) {
				(t[n] = 255 & e),
					(t[n + 1] = (e >>> 8) & 255),
					(t[n + 2] = (e >>> 16) & 255),
					(t[n + 3] = e >>> 24);
			}
			(f.create = p()),
				(f.alloc = function (e) {
					return new i.Array(e);
				}),
				i.Array !== Array &&
					(f.alloc = i.pool(f.alloc, i.Array.prototype.subarray)),
				(f.prototype._push = function (e, t, n) {
					return (
						(this.tail = this.tail.next = new u(e, t, n)), (this.len += t), this
					);
				}),
				(g.prototype = Object.create(u.prototype)),
				(g.prototype.fn = function (e, t, n) {
					for (; e > 127; ) (t[n++] = (127 & e) | 128), (e >>>= 7);
					t[n] = e;
				}),
				(f.prototype.uint32 = function (e) {
					return (
						(this.len += (this.tail = this.tail.next =
							new g(
								(e >>>= 0) < 128
									? 1
									: e < 16384
									? 2
									: e < 2097152
									? 3
									: e < 268435456
									? 4
									: 5,
								e
							)).len),
						this
					);
				}),
				(f.prototype.int32 = function (e) {
					return e < 0 ? this._push(d, 10, o.fromNumber(e)) : this.uint32(e);
				}),
				(f.prototype.sint32 = function (e) {
					return this.uint32(((e << 1) ^ (e >> 31)) >>> 0);
				}),
				(f.prototype.uint64 = function (e) {
					var t = o.from(e);
					return this._push(d, t.length(), t);
				}),
				(f.prototype.int64 = f.prototype.uint64),
				(f.prototype.sint64 = function (e) {
					var t = o.from(e).zzEncode();
					return this._push(d, t.length(), t);
				}),
				(f.prototype.bool = function (e) {
					return this._push(h, 1, e ? 1 : 0);
				}),
				(f.prototype.fixed32 = function (e) {
					return this._push(y, 4, e >>> 0);
				}),
				(f.prototype.sfixed32 = f.prototype.fixed32),
				(f.prototype.fixed64 = function (e) {
					var t = o.from(e);
					return this._push(y, 4, t.lo)._push(y, 4, t.hi);
				}),
				(f.prototype.sfixed64 = f.prototype.fixed64),
				(f.prototype.float = function (e) {
					return this._push(i.float.writeFloatLE, 4, e);
				}),
				(f.prototype.double = function (e) {
					return this._push(i.float.writeDoubleLE, 8, e);
				});
			var m = i.Array.prototype.set
				? function (e, t, n) {
						t.set(e, n);
				  }
				: function (e, t, n) {
						for (var r = 0; r < e.length; ++r) t[n + r] = e[r];
				  };
			(f.prototype.bytes = function (e) {
				var t = e.length >>> 0;
				if (!t) return this._push(h, 1, 0);
				if (i.isString(e)) {
					var n = f.alloc((t = s.length(e)));
					s.decode(e, n, 0), (e = n);
				}
				return this.uint32(t)._push(m, t, e);
			}),
				(f.prototype.string = function (e) {
					var t = a.length(e);
					return t ? this.uint32(t)._push(a.write, t, e) : this._push(h, 1, 0);
				}),
				(f.prototype.fork = function () {
					return (
						(this.states = new l(this)),
						(this.head = this.tail = new u(c, 0, 0)),
						(this.len = 0),
						this
					);
				}),
				(f.prototype.reset = function () {
					return (
						this.states
							? ((this.head = this.states.head),
							  (this.tail = this.states.tail),
							  (this.len = this.states.len),
							  (this.states = this.states.next))
							: ((this.head = this.tail = new u(c, 0, 0)), (this.len = 0)),
						this
					);
				}),
				(f.prototype.ldelim = function () {
					var e = this.head,
						t = this.tail,
						n = this.len;
					return (
						this.reset().uint32(n),
						n && ((this.tail.next = e.next), (this.tail = t), (this.len += n)),
						this
					);
				}),
				(f.prototype.finish = function () {
					for (
						var e = this.head.next, t = this.constructor.alloc(this.len), n = 0;
						e;

					)
						e.fn(e.val, t, n), (n += e.len), (e = e.next);
					return t;
				}),
				(f._configure = function (e) {
					(r = e), (f.create = p()), r._configure();
				});
		},
		function (e, t, n) {
			"use strict";
			e.exports = u;
			var r,
				i = n(7),
				o = i.LongBits,
				s = i.utf8;
			function a(e, t) {
				return RangeError(
					"index out of range: " + e.pos + " + " + (t || 1) + " > " + e.len
				);
			}
			function u(e) {
				(this.buf = e), (this.pos = 0), (this.len = e.length);
			}
			var c,
				l =
					"undefined" != typeof Uint8Array
						? function (e) {
								if (e instanceof Uint8Array || Array.isArray(e))
									return new u(e);
								throw Error("illegal buffer");
						  }
						: function (e) {
								if (Array.isArray(e)) return new u(e);
								throw Error("illegal buffer");
						  },
				f = function () {
					return i.Buffer
						? function (e) {
								return (u.create = function (e) {
									return i.Buffer.isBuffer(e) ? new r(e) : l(e);
								})(e);
						  }
						: l;
				};
			function p() {
				var e = new o(0, 0),
					t = 0;
				if (!(this.len - this.pos > 4)) {
					for (; t < 3; ++t) {
						if (this.pos >= this.len) throw a(this);
						if (
							((e.lo = (e.lo | ((127 & this.buf[this.pos]) << (7 * t))) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return e;
					}
					return (
						(e.lo = (e.lo | ((127 & this.buf[this.pos++]) << (7 * t))) >>> 0), e
					);
				}
				for (; t < 4; ++t)
					if (
						((e.lo = (e.lo | ((127 & this.buf[this.pos]) << (7 * t))) >>> 0),
						this.buf[this.pos++] < 128)
					)
						return e;
				if (
					((e.lo = (e.lo | ((127 & this.buf[this.pos]) << 28)) >>> 0),
					(e.hi = (e.hi | ((127 & this.buf[this.pos]) >> 4)) >>> 0),
					this.buf[this.pos++] < 128)
				)
					return e;
				if (((t = 0), this.len - this.pos > 4)) {
					for (; t < 5; ++t)
						if (
							((e.hi =
								(e.hi | ((127 & this.buf[this.pos]) << (7 * t + 3))) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return e;
				} else
					for (; t < 5; ++t) {
						if (this.pos >= this.len) throw a(this);
						if (
							((e.hi =
								(e.hi | ((127 & this.buf[this.pos]) << (7 * t + 3))) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return e;
					}
				throw Error("invalid varint encoding");
			}
			function h(e, t) {
				return (
					(e[t - 4] | (e[t - 3] << 8) | (e[t - 2] << 16) | (e[t - 1] << 24)) >>>
					0
				);
			}
			function g() {
				if (this.pos + 8 > this.len) throw a(this, 8);
				return new o(
					h(this.buf, (this.pos += 4)),
					h(this.buf, (this.pos += 4))
				);
			}
			(u.create = f()),
				(u.prototype._slice =
					i.Array.prototype.subarray || i.Array.prototype.slice),
				(u.prototype.uint32 =
					((c = 4294967295),
					function () {
						if (
							((c = (127 & this.buf[this.pos]) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return c;
						if (
							((c = (c | ((127 & this.buf[this.pos]) << 7)) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return c;
						if (
							((c = (c | ((127 & this.buf[this.pos]) << 14)) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return c;
						if (
							((c = (c | ((127 & this.buf[this.pos]) << 21)) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return c;
						if (
							((c = (c | ((15 & this.buf[this.pos]) << 28)) >>> 0),
							this.buf[this.pos++] < 128)
						)
							return c;
						if ((this.pos += 5) > this.len)
							throw ((this.pos = this.len), a(this, 10));
						return c;
					})),
				(u.prototype.int32 = function () {
					return 0 | this.uint32();
				}),
				(u.prototype.sint32 = function () {
					var e = this.uint32();
					return ((e >>> 1) ^ -(1 & e)) | 0;
				}),
				(u.prototype.bool = function () {
					return 0 !== this.uint32();
				}),
				(u.prototype.fixed32 = function () {
					if (this.pos + 4 > this.len) throw a(this, 4);
					return h(this.buf, (this.pos += 4));
				}),
				(u.prototype.sfixed32 = function () {
					if (this.pos + 4 > this.len) throw a(this, 4);
					return 0 | h(this.buf, (this.pos += 4));
				}),
				(u.prototype.float = function () {
					if (this.pos + 4 > this.len) throw a(this, 4);
					var e = i.float.readFloatLE(this.buf, this.pos);
					return (this.pos += 4), e;
				}),
				(u.prototype.double = function () {
					if (this.pos + 8 > this.len) throw a(this, 4);
					var e = i.float.readDoubleLE(this.buf, this.pos);
					return (this.pos += 8), e;
				}),
				(u.prototype.bytes = function () {
					var e = this.uint32(),
						t = this.pos,
						n = this.pos + e;
					if (n > this.len) throw a(this, e);
					return (
						(this.pos += e),
						Array.isArray(this.buf)
							? this.buf.slice(t, n)
							: t === n
							? new this.buf.constructor(0)
							: this._slice.call(this.buf, t, n)
					);
				}),
				(u.prototype.string = function () {
					var e = this.bytes();
					return s.read(e, 0, e.length);
				}),
				(u.prototype.skip = function (e) {
					if ("number" == typeof e) {
						if (this.pos + e > this.len) throw a(this, e);
						this.pos += e;
					} else
						do {
							if (this.pos >= this.len) throw a(this);
						} while (128 & this.buf[this.pos++]);
					return this;
				}),
				(u.prototype.skipType = function (e) {
					switch (e) {
						case 0:
							this.skip();
							break;
						case 1:
							this.skip(8);
							break;
						case 2:
							this.skip(this.uint32());
							break;
						case 3:
							for (; 4 != (e = 7 & this.uint32()); ) this.skipType(e);
							break;
						case 5:
							this.skip(4);
							break;
						default:
							throw Error("invalid wire type " + e + " at offset " + this.pos);
					}
					return this;
				}),
				(u._configure = function (e) {
					(r = e), (u.create = f()), r._configure();
					var t = i.Long ? "toLong" : "toNumber";
					i.merge(u.prototype, {
						int64: function () {
							return p.call(this)[t](!1);
						},
						uint64: function () {
							return p.call(this)[t](!0);
						},
						sint64: function () {
							return p.call(this).zzDecode()[t](!1);
						},
						fixed64: function () {
							return g.call(this)[t](!0);
						},
						sfixed64: function () {
							return g.call(this)[t](!1);
						},
					});
				});
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.isFunction = function (e) {
					return "function" == typeof e;
				});
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = n(13),
				i = n(22);
			t.empty = {
				closed: !0,
				next: function (e) {},
				error: function (e) {
					if (r.config.useDeprecatedSynchronousErrorHandling) throw e;
					i.hostReportError(e);
				},
				complete: function () {},
			};
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.hostReportError = function (e) {
					setTimeout(function () {
						throw e;
					}, 0);
				});
		},
		function (e, t, n) {
			"use strict";
			(t.decode = t.parse = n(39)), (t.encode = t.stringify = n(40));
		},
		function (e, t) {
			e.exports = function (e) {
				return (
					e.webpackPolyfill ||
						((e.deprecate = function () {}),
						(e.paths = []),
						e.children || (e.children = []),
						Object.defineProperty(e, "loaded", {
							enumerable: !0,
							get: function () {
								return e.l;
							},
						}),
						Object.defineProperty(e, "id", {
							enumerable: !0,
							get: function () {
								return e.i;
							},
						}),
						(e.webpackPolyfill = 1)),
					e
				);
			};
		},
		function (e, t, n) {
			"use strict";
			var r = t;
			function i() {
				r.util._configure(),
					r.Writer._configure(r.BufferWriter),
					r.Reader._configure(r.BufferReader);
			}
			(r.build = "minimal"),
				(r.Writer = n(18)),
				(r.BufferWriter = n(34)),
				(r.Reader = n(19)),
				(r.BufferReader = n(35)),
				(r.util = n(7)),
				(r.rpc = n(36)),
				(r.roots = n(38)),
				(r.configure = i),
				i();
		},
		function (e, t, n) {
			"use strict";
			e.exports = function (e, t) {
				var n = new Array(arguments.length - 1),
					r = 0,
					i = 2,
					o = !0;
				for (; i < arguments.length; ) n[r++] = arguments[i++];
				return new Promise(function (i, s) {
					n[r] = function (e) {
						if (o)
							if (((o = !1), e)) s(e);
							else {
								for (
									var t = new Array(arguments.length - 1), n = 0;
									n < t.length;

								)
									t[n++] = arguments[n];
								i.apply(null, t);
							}
					};
					try {
						e.apply(t || null, n);
					} catch (e) {
						o && ((o = !1), s(e));
					}
				});
			};
		},
		function (e, t, n) {
			"use strict";
			var r = t;
			r.length = function (e) {
				var t = e.length;
				if (!t) return 0;
				for (var n = 0; --t % 4 > 1 && "=" === e.charAt(t); ) ++n;
				return Math.ceil(3 * e.length) / 4 - n;
			};
			for (var i = new Array(64), o = new Array(123), s = 0; s < 64; )
				o[
					(i[s] =
						s < 26 ? s + 65 : s < 52 ? s + 71 : s < 62 ? s - 4 : (s - 59) | 43)
				] = s++;
			r.encode = function (e, t, n) {
				for (var r, o = null, s = [], a = 0, u = 0; t < n; ) {
					var c = e[t++];
					switch (u) {
						case 0:
							(s[a++] = i[c >> 2]), (r = (3 & c) << 4), (u = 1);
							break;
						case 1:
							(s[a++] = i[r | (c >> 4)]), (r = (15 & c) << 2), (u = 2);
							break;
						case 2:
							(s[a++] = i[r | (c >> 6)]), (s[a++] = i[63 & c]), (u = 0);
					}
					a > 8191 &&
						((o || (o = [])).push(String.fromCharCode.apply(String, s)),
						(a = 0));
				}
				return (
					u && ((s[a++] = i[r]), (s[a++] = 61), 1 === u && (s[a++] = 61)),
					o
						? (a && o.push(String.fromCharCode.apply(String, s.slice(0, a))),
						  o.join(""))
						: String.fromCharCode.apply(String, s.slice(0, a))
				);
			};
			(r.decode = function (e, t, n) {
				for (var r, i = n, s = 0, a = 0; a < e.length; ) {
					var u = e.charCodeAt(a++);
					if (61 === u && s > 1) break;
					if (void 0 === (u = o[u])) throw Error("invalid encoding");
					switch (s) {
						case 0:
							(r = u), (s = 1);
							break;
						case 1:
							(t[n++] = (r << 2) | ((48 & u) >> 4)), (r = u), (s = 2);
							break;
						case 2:
							(t[n++] = ((15 & r) << 4) | ((60 & u) >> 2)), (r = u), (s = 3);
							break;
						case 3:
							(t[n++] = ((3 & r) << 6) | u), (s = 0);
					}
				}
				if (1 === s) throw Error("invalid encoding");
				return n - i;
			}),
				(r.test = function (e) {
					return /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(
						e
					);
				});
		},
		function (e, t, n) {
			"use strict";
			function r() {
				this._listeners = {};
			}
			(e.exports = r),
				(r.prototype.on = function (e, t, n) {
					return (
						(this._listeners[e] || (this._listeners[e] = [])).push({
							fn: t,
							ctx: n || this,
						}),
						this
					);
				}),
				(r.prototype.off = function (e, t) {
					if (void 0 === e) this._listeners = {};
					else if (void 0 === t) this._listeners[e] = [];
					else
						for (var n = this._listeners[e], r = 0; r < n.length; )
							n[r].fn === t ? n.splice(r, 1) : ++r;
					return this;
				}),
				(r.prototype.emit = function (e) {
					var t = this._listeners[e];
					if (t) {
						for (var n = [], r = 1; r < arguments.length; )
							n.push(arguments[r++]);
						for (r = 0; r < t.length; ) t[r].fn.apply(t[r++].ctx, n);
					}
					return this;
				});
		},
		function (e, t, n) {
			"use strict";
			function r(e) {
				return (
					"undefined" != typeof Float32Array
						? (function () {
								var t = new Float32Array([-0]),
									n = new Uint8Array(t.buffer),
									r = 128 === n[3];
								function i(e, r, i) {
									(t[0] = e),
										(r[i] = n[0]),
										(r[i + 1] = n[1]),
										(r[i + 2] = n[2]),
										(r[i + 3] = n[3]);
								}
								function o(e, r, i) {
									(t[0] = e),
										(r[i] = n[3]),
										(r[i + 1] = n[2]),
										(r[i + 2] = n[1]),
										(r[i + 3] = n[0]);
								}
								function s(e, r) {
									return (
										(n[0] = e[r]),
										(n[1] = e[r + 1]),
										(n[2] = e[r + 2]),
										(n[3] = e[r + 3]),
										t[0]
									);
								}
								function a(e, r) {
									return (
										(n[3] = e[r]),
										(n[2] = e[r + 1]),
										(n[1] = e[r + 2]),
										(n[0] = e[r + 3]),
										t[0]
									);
								}
								(e.writeFloatLE = r ? i : o),
									(e.writeFloatBE = r ? o : i),
									(e.readFloatLE = r ? s : a),
									(e.readFloatBE = r ? a : s);
						  })()
						: (function () {
								function t(e, t, n, r) {
									var i = t < 0 ? 1 : 0;
									if ((i && (t = -t), 0 === t))
										e(1 / t > 0 ? 0 : 2147483648, n, r);
									else if (isNaN(t)) e(2143289344, n, r);
									else if (t > 34028234663852886e22)
										e(((i << 31) | 2139095040) >>> 0, n, r);
									else if (t < 11754943508222875e-54)
										e(
											((i << 31) | Math.round(t / 1401298464324817e-60)) >>> 0,
											n,
											r
										);
									else {
										var o = Math.floor(Math.log(t) / Math.LN2);
										e(
											((i << 31) |
												((o + 127) << 23) |
												(8388607 &
													Math.round(t * Math.pow(2, -o) * 8388608))) >>>
												0,
											n,
											r
										);
									}
								}
								function n(e, t, n) {
									var r = e(t, n),
										i = 2 * (r >> 31) + 1,
										o = (r >>> 23) & 255,
										s = 8388607 & r;
									return 255 === o
										? s
											? NaN
											: i * (1 / 0)
										: 0 === o
										? 1401298464324817e-60 * i * s
										: i * Math.pow(2, o - 150) * (s + 8388608);
								}
								(e.writeFloatLE = t.bind(null, i)),
									(e.writeFloatBE = t.bind(null, o)),
									(e.readFloatLE = n.bind(null, s)),
									(e.readFloatBE = n.bind(null, a));
						  })(),
					"undefined" != typeof Float64Array
						? (function () {
								var t = new Float64Array([-0]),
									n = new Uint8Array(t.buffer),
									r = 128 === n[7];
								function i(e, r, i) {
									(t[0] = e),
										(r[i] = n[0]),
										(r[i + 1] = n[1]),
										(r[i + 2] = n[2]),
										(r[i + 3] = n[3]),
										(r[i + 4] = n[4]),
										(r[i + 5] = n[5]),
										(r[i + 6] = n[6]),
										(r[i + 7] = n[7]);
								}
								function o(e, r, i) {
									(t[0] = e),
										(r[i] = n[7]),
										(r[i + 1] = n[6]),
										(r[i + 2] = n[5]),
										(r[i + 3] = n[4]),
										(r[i + 4] = n[3]),
										(r[i + 5] = n[2]),
										(r[i + 6] = n[1]),
										(r[i + 7] = n[0]);
								}
								function s(e, r) {
									return (
										(n[0] = e[r]),
										(n[1] = e[r + 1]),
										(n[2] = e[r + 2]),
										(n[3] = e[r + 3]),
										(n[4] = e[r + 4]),
										(n[5] = e[r + 5]),
										(n[6] = e[r + 6]),
										(n[7] = e[r + 7]),
										t[0]
									);
								}
								function a(e, r) {
									return (
										(n[7] = e[r]),
										(n[6] = e[r + 1]),
										(n[5] = e[r + 2]),
										(n[4] = e[r + 3]),
										(n[3] = e[r + 4]),
										(n[2] = e[r + 5]),
										(n[1] = e[r + 6]),
										(n[0] = e[r + 7]),
										t[0]
									);
								}
								(e.writeDoubleLE = r ? i : o),
									(e.writeDoubleBE = r ? o : i),
									(e.readDoubleLE = r ? s : a),
									(e.readDoubleBE = r ? a : s);
						  })()
						: (function () {
								function t(e, t, n, r, i, o) {
									var s = r < 0 ? 1 : 0;
									if ((s && (r = -r), 0 === r))
										e(0, i, o + t), e(1 / r > 0 ? 0 : 2147483648, i, o + n);
									else if (isNaN(r)) e(0, i, o + t), e(2146959360, i, o + n);
									else if (r > 17976931348623157e292)
										e(0, i, o + t), e(((s << 31) | 2146435072) >>> 0, i, o + n);
									else {
										var a;
										if (r < 22250738585072014e-324)
											e((a = r / 5e-324) >>> 0, i, o + t),
												e(((s << 31) | (a / 4294967296)) >>> 0, i, o + n);
										else {
											var u = Math.floor(Math.log(r) / Math.LN2);
											1024 === u && (u = 1023),
												e(
													(4503599627370496 * (a = r * Math.pow(2, -u))) >>> 0,
													i,
													o + t
												),
												e(
													((s << 31) |
														((u + 1023) << 20) |
														((1048576 * a) & 1048575)) >>>
														0,
													i,
													o + n
												);
										}
									}
								}
								function n(e, t, n, r, i) {
									var o = e(r, i + t),
										s = e(r, i + n),
										a = 2 * (s >> 31) + 1,
										u = (s >>> 20) & 2047,
										c = 4294967296 * (1048575 & s) + o;
									return 2047 === u
										? c
											? NaN
											: a * (1 / 0)
										: 0 === u
										? 5e-324 * a * c
										: a * Math.pow(2, u - 1075) * (c + 4503599627370496);
								}
								(e.writeDoubleLE = t.bind(null, i, 0, 4)),
									(e.writeDoubleBE = t.bind(null, o, 4, 0)),
									(e.readDoubleLE = n.bind(null, s, 0, 4)),
									(e.readDoubleBE = n.bind(null, a, 4, 0));
						  })(),
					e
				);
			}
			function i(e, t, n) {
				(t[n] = 255 & e),
					(t[n + 1] = (e >>> 8) & 255),
					(t[n + 2] = (e >>> 16) & 255),
					(t[n + 3] = e >>> 24);
			}
			function o(e, t, n) {
				(t[n] = e >>> 24),
					(t[n + 1] = (e >>> 16) & 255),
					(t[n + 2] = (e >>> 8) & 255),
					(t[n + 3] = 255 & e);
			}
			function s(e, t) {
				return (
					(e[t] | (e[t + 1] << 8) | (e[t + 2] << 16) | (e[t + 3] << 24)) >>> 0
				);
			}
			function a(e, t) {
				return (
					((e[t] << 24) | (e[t + 1] << 16) | (e[t + 2] << 8) | e[t + 3]) >>> 0
				);
			}
			e.exports = r(r);
		},
		function (module, exports, __webpack_require__) {
			"use strict";
			function inquire(moduleName) {
				try {
					var mod = eval("quire".replace(/^/, "re"))(moduleName);
					if (mod && (mod.length || Object.keys(mod).length)) return mod;
				} catch (e) {}
				return null;
			}
			module.exports = inquire;
		},
		function (e, t, n) {
			"use strict";
			var r = t;
			(r.length = function (e) {
				for (var t = 0, n = 0, r = 0; r < e.length; ++r)
					(n = e.charCodeAt(r)) < 128
						? (t += 1)
						: n < 2048
						? (t += 2)
						: 55296 == (64512 & n) && 56320 == (64512 & e.charCodeAt(r + 1))
						? (++r, (t += 4))
						: (t += 3);
				return t;
			}),
				(r.read = function (e, t, n) {
					if (n - t < 1) return "";
					for (var r, i = null, o = [], s = 0; t < n; )
						(r = e[t++]) < 128
							? (o[s++] = r)
							: r > 191 && r < 224
							? (o[s++] = ((31 & r) << 6) | (63 & e[t++]))
							: r > 239 && r < 365
							? ((r =
									(((7 & r) << 18) |
										((63 & e[t++]) << 12) |
										((63 & e[t++]) << 6) |
										(63 & e[t++])) -
									65536),
							  (o[s++] = 55296 + (r >> 10)),
							  (o[s++] = 56320 + (1023 & r)))
							: (o[s++] =
									((15 & r) << 12) | ((63 & e[t++]) << 6) | (63 & e[t++])),
							s > 8191 &&
								((i || (i = [])).push(String.fromCharCode.apply(String, o)),
								(s = 0));
					return i
						? (s && i.push(String.fromCharCode.apply(String, o.slice(0, s))),
						  i.join(""))
						: String.fromCharCode.apply(String, o.slice(0, s));
				}),
				(r.write = function (e, t, n) {
					for (var r, i, o = n, s = 0; s < e.length; ++s)
						(r = e.charCodeAt(s)) < 128
							? (t[n++] = r)
							: r < 2048
							? ((t[n++] = (r >> 6) | 192), (t[n++] = (63 & r) | 128))
							: 55296 == (64512 & r) &&
							  56320 == (64512 & (i = e.charCodeAt(s + 1)))
							? ((r = 65536 + ((1023 & r) << 10) + (1023 & i)),
							  ++s,
							  (t[n++] = (r >> 18) | 240),
							  (t[n++] = ((r >> 12) & 63) | 128),
							  (t[n++] = ((r >> 6) & 63) | 128),
							  (t[n++] = (63 & r) | 128))
							: ((t[n++] = (r >> 12) | 224),
							  (t[n++] = ((r >> 6) & 63) | 128),
							  (t[n++] = (63 & r) | 128));
					return n - o;
				});
		},
		function (e, t, n) {
			"use strict";
			e.exports = function (e, t, n) {
				var r = n || 8192,
					i = r >>> 1,
					o = null,
					s = r;
				return function (n) {
					if (n < 1 || n > i) return e(n);
					s + n > r && ((o = e(r)), (s = 0));
					var a = t.call(o, s, (s += n));
					return 7 & s && (s = 1 + (7 | s)), a;
				};
			};
		},
		function (e, t, n) {
			"use strict";
			e.exports = i;
			var r = n(7);
			function i(e, t) {
				(this.lo = e >>> 0), (this.hi = t >>> 0);
			}
			var o = (i.zero = new i(0, 0));
			(o.toNumber = function () {
				return 0;
			}),
				(o.zzEncode = o.zzDecode =
					function () {
						return this;
					}),
				(o.length = function () {
					return 1;
				});
			var s = (i.zeroHash = "\0\0\0\0\0\0\0\0");
			(i.fromNumber = function (e) {
				if (0 === e) return o;
				var t = e < 0;
				t && (e = -e);
				var n = e >>> 0,
					r = ((e - n) / 4294967296) >>> 0;
				return (
					t &&
						((r = ~r >>> 0),
						(n = ~n >>> 0),
						++n > 4294967295 && ((n = 0), ++r > 4294967295 && (r = 0))),
					new i(n, r)
				);
			}),
				(i.from = function (e) {
					if ("number" == typeof e) return i.fromNumber(e);
					if (r.isString(e)) {
						if (!r.Long) return i.fromNumber(parseInt(e, 10));
						e = r.Long.fromString(e);
					}
					return e.low || e.high ? new i(e.low >>> 0, e.high >>> 0) : o;
				}),
				(i.prototype.toNumber = function (e) {
					if (!e && this.hi >>> 31) {
						var t = (1 + ~this.lo) >>> 0,
							n = ~this.hi >>> 0;
						return t || (n = (n + 1) >>> 0), -(t + 4294967296 * n);
					}
					return this.lo + 4294967296 * this.hi;
				}),
				(i.prototype.toLong = function (e) {
					return r.Long
						? new r.Long(0 | this.lo, 0 | this.hi, Boolean(e))
						: { low: 0 | this.lo, high: 0 | this.hi, unsigned: Boolean(e) };
				});
			var a = String.prototype.charCodeAt;
			(i.fromHash = function (e) {
				return e === s
					? o
					: new i(
							(a.call(e, 0) |
								(a.call(e, 1) << 8) |
								(a.call(e, 2) << 16) |
								(a.call(e, 3) << 24)) >>>
								0,
							(a.call(e, 4) |
								(a.call(e, 5) << 8) |
								(a.call(e, 6) << 16) |
								(a.call(e, 7) << 24)) >>>
								0
					  );
			}),
				(i.prototype.toHash = function () {
					return String.fromCharCode(
						255 & this.lo,
						(this.lo >>> 8) & 255,
						(this.lo >>> 16) & 255,
						this.lo >>> 24,
						255 & this.hi,
						(this.hi >>> 8) & 255,
						(this.hi >>> 16) & 255,
						this.hi >>> 24
					);
				}),
				(i.prototype.zzEncode = function () {
					var e = this.hi >> 31;
					return (
						(this.hi = (((this.hi << 1) | (this.lo >>> 31)) ^ e) >>> 0),
						(this.lo = ((this.lo << 1) ^ e) >>> 0),
						this
					);
				}),
				(i.prototype.zzDecode = function () {
					var e = -(1 & this.lo);
					return (
						(this.lo = (((this.lo >>> 1) | (this.hi << 31)) ^ e) >>> 0),
						(this.hi = ((this.hi >>> 1) ^ e) >>> 0),
						this
					);
				}),
				(i.prototype.length = function () {
					var e = this.lo,
						t = ((this.lo >>> 28) | (this.hi << 4)) >>> 0,
						n = this.hi >>> 24;
					return 0 === n
						? 0 === t
							? e < 16384
								? e < 128
									? 1
									: 2
								: e < 2097152
								? 3
								: 4
							: t < 16384
							? t < 128
								? 5
								: 6
							: t < 2097152
							? 7
							: 8
						: n < 128
						? 9
						: 10;
				});
		},
		function (e, t, n) {
			"use strict";
			e.exports = o;
			var r = n(18);
			(o.prototype = Object.create(r.prototype)).constructor = o;
			var i = n(7);
			function o() {
				r.call(this);
			}
			function s(e, t, n) {
				e.length < 40
					? i.utf8.write(e, t, n)
					: t.utf8Write
					? t.utf8Write(e, n)
					: t.write(e, n);
			}
			(o._configure = function () {
				(o.alloc = i._Buffer_allocUnsafe),
					(o.writeBytesBuffer =
						i.Buffer &&
						i.Buffer.prototype instanceof Uint8Array &&
						"set" === i.Buffer.prototype.set.name
							? function (e, t, n) {
									t.set(e, n);
							  }
							: function (e, t, n) {
									if (e.copy) e.copy(t, n, 0, e.length);
									else for (var r = 0; r < e.length; ) t[n++] = e[r++];
							  });
			}),
				(o.prototype.bytes = function (e) {
					i.isString(e) && (e = i._Buffer_from(e, "base64"));
					var t = e.length >>> 0;
					return (
						this.uint32(t), t && this._push(o.writeBytesBuffer, t, e), this
					);
				}),
				(o.prototype.string = function (e) {
					var t = i.Buffer.byteLength(e);
					return this.uint32(t), t && this._push(s, t, e), this;
				}),
				o._configure();
		},
		function (e, t, n) {
			"use strict";
			e.exports = o;
			var r = n(19);
			(o.prototype = Object.create(r.prototype)).constructor = o;
			var i = n(7);
			function o(e) {
				r.call(this, e);
			}
			(o._configure = function () {
				i.Buffer && (o.prototype._slice = i.Buffer.prototype.slice);
			}),
				(o.prototype.string = function () {
					var e = this.uint32();
					return this.buf.utf8Slice
						? this.buf.utf8Slice(
								this.pos,
								(this.pos = Math.min(this.pos + e, this.len))
						  )
						: this.buf.toString(
								"utf-8",
								this.pos,
								(this.pos = Math.min(this.pos + e, this.len))
						  );
				}),
				o._configure();
		},
		function (e, t, n) {
			"use strict";
			t.Service = n(37);
		},
		function (e, t, n) {
			"use strict";
			e.exports = i;
			var r = n(7);
			function i(e, t, n) {
				if ("function" != typeof e)
					throw TypeError("rpcImpl must be a function");
				r.EventEmitter.call(this),
					(this.rpcImpl = e),
					(this.requestDelimited = Boolean(t)),
					(this.responseDelimited = Boolean(n));
			}
			((i.prototype = Object.create(r.EventEmitter.prototype)).constructor = i),
				(i.prototype.rpcCall = function e(t, n, i, o, s) {
					if (!o) throw TypeError("request must be specified");
					var a = this;
					if (!s) return r.asPromise(e, a, t, n, i, o);
					if (a.rpcImpl)
						try {
							return a.rpcImpl(
								t,
								n[a.requestDelimited ? "encodeDelimited" : "encode"](
									o
								).finish(),
								function (e, n) {
									if (e) return a.emit("error", e, t), s(e);
									if (null !== n) {
										if (!(n instanceof i))
											try {
												n =
													i[a.responseDelimited ? "decodeDelimited" : "decode"](
														n
													);
											} catch (e) {
												return a.emit("error", e, t), s(e);
											}
										return a.emit("data", n, t), s(null, n);
									}
									a.end(!0);
								}
							);
						} catch (e) {
							return (
								a.emit("error", e, t),
								void setTimeout(function () {
									s(e);
								}, 0)
							);
						}
					else
						setTimeout(function () {
							s(Error("already ended"));
						}, 0);
				}),
				(i.prototype.end = function (e) {
					return (
						this.rpcImpl &&
							(e || this.rpcImpl(null, null, null),
							(this.rpcImpl = null),
							this.emit("end").off()),
						this
					);
				});
		},
		function (e, t, n) {
			"use strict";
			e.exports = {};
		},
		function (e, t, n) {
			"use strict";
			function r(e, t) {
				return Object.prototype.hasOwnProperty.call(e, t);
			}
			e.exports = function (e, t, n, o) {
				(t = t || "&"), (n = n || "=");
				var s = {};
				if ("string" != typeof e || 0 === e.length) return s;
				var a = /\+/g;
				e = e.split(t);
				var u = 1e3;
				o && "number" == typeof o.maxKeys && (u = o.maxKeys);
				var c = e.length;
				u > 0 && c > u && (c = u);
				for (var l = 0; l < c; ++l) {
					var f,
						p,
						h,
						g,
						d = e[l].replace(a, "%20"),
						y = d.indexOf(n);
					y >= 0
						? ((f = d.substr(0, y)), (p = d.substr(y + 1)))
						: ((f = d), (p = "")),
						(h = decodeURIComponent(f)),
						(g = decodeURIComponent(p)),
						r(s, h)
							? i(s[h])
								? s[h].push(g)
								: (s[h] = [s[h], g])
							: (s[h] = g);
				}
				return s;
			};
			var i =
				Array.isArray ||
				function (e) {
					return "[object Array]" === Object.prototype.toString.call(e);
				};
		},
		function (e, t, n) {
			"use strict";
			var r = function (e) {
				switch (typeof e) {
					case "string":
						return e;
					case "boolean":
						return e ? "true" : "false";
					case "number":
						return isFinite(e) ? e : "";
					default:
						return "";
				}
			};
			e.exports = function (e, t, n, a) {
				return (
					(t = t || "&"),
					(n = n || "="),
					null === e && (e = void 0),
					"object" == typeof e
						? o(s(e), function (s) {
								var a = encodeURIComponent(r(s)) + n;
								return i(e[s])
									? o(e[s], function (e) {
											return a + encodeURIComponent(r(e));
									  }).join(t)
									: a + encodeURIComponent(r(e[s]));
						  }).join(t)
						: a
						? encodeURIComponent(r(a)) + n + encodeURIComponent(r(e))
						: ""
				);
			};
			var i =
				Array.isArray ||
				function (e) {
					return "[object Array]" === Object.prototype.toString.call(e);
				};
			function o(e, t) {
				if (e.map) return e.map(t);
				for (var n = [], r = 0; r < e.length; r++) n.push(t(e[r], r));
				return n;
			}
			var s =
				Object.keys ||
				function (e) {
					var t = [];
					for (var n in e)
						Object.prototype.hasOwnProperty.call(e, n) && t.push(n);
					return t;
				};
		},
		function (e, t, n) {
			"use strict";
			(t.byteLength = function (e) {
				var t = c(e),
					n = t[0],
					r = t[1];
				return (3 * (n + r)) / 4 - r;
			}),
				(t.toByteArray = function (e) {
					var t,
						n,
						r = c(e),
						s = r[0],
						a = r[1],
						u = new o(
							(function (e, t, n) {
								return (3 * (t + n)) / 4 - n;
							})(0, s, a)
						),
						l = 0,
						f = a > 0 ? s - 4 : s;
					for (n = 0; n < f; n += 4)
						(t =
							(i[e.charCodeAt(n)] << 18) |
							(i[e.charCodeAt(n + 1)] << 12) |
							(i[e.charCodeAt(n + 2)] << 6) |
							i[e.charCodeAt(n + 3)]),
							(u[l++] = (t >> 16) & 255),
							(u[l++] = (t >> 8) & 255),
							(u[l++] = 255 & t);
					2 === a &&
						((t = (i[e.charCodeAt(n)] << 2) | (i[e.charCodeAt(n + 1)] >> 4)),
						(u[l++] = 255 & t));
					1 === a &&
						((t =
							(i[e.charCodeAt(n)] << 10) |
							(i[e.charCodeAt(n + 1)] << 4) |
							(i[e.charCodeAt(n + 2)] >> 2)),
						(u[l++] = (t >> 8) & 255),
						(u[l++] = 255 & t));
					return u;
				}),
				(t.fromByteArray = function (e) {
					for (
						var t, n = e.length, i = n % 3, o = [], s = 0, a = n - i;
						s < a;
						s += 16383
					)
						o.push(l(e, s, s + 16383 > a ? a : s + 16383));
					1 === i
						? ((t = e[n - 1]), o.push(r[t >> 2] + r[(t << 4) & 63] + "=="))
						: 2 === i &&
						  ((t = (e[n - 2] << 8) + e[n - 1]),
						  o.push(r[t >> 10] + r[(t >> 4) & 63] + r[(t << 2) & 63] + "="));
					return o.join("");
				});
			for (
				var r = [],
					i = [],
					o = "undefined" != typeof Uint8Array ? Uint8Array : Array,
					s =
						"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
					a = 0,
					u = s.length;
				a < u;
				++a
			)
				(r[a] = s[a]), (i[s.charCodeAt(a)] = a);
			function c(e) {
				var t = e.length;
				if (t % 4 > 0)
					throw new Error("Invalid string. Length must be a multiple of 4");
				var n = e.indexOf("=");
				return -1 === n && (n = t), [n, n === t ? 0 : 4 - (n % 4)];
			}
			function l(e, t, n) {
				for (var i, o, s = [], a = t; a < n; a += 3)
					(i =
						((e[a] << 16) & 16711680) +
						((e[a + 1] << 8) & 65280) +
						(255 & e[a + 2])),
						s.push(
							r[((o = i) >> 18) & 63] +
								r[(o >> 12) & 63] +
								r[(o >> 6) & 63] +
								r[63 & o]
						);
				return s.join("");
			}
			(i["-".charCodeAt(0)] = 62), (i["_".charCodeAt(0)] = 63);
		},
		function (e, t) {
			/*! ieee754. BSD-3-Clause License. Feross Aboukhadijeh <https://feross.org/opensource> */
			(t.read = function (e, t, n, r, i) {
				var o,
					s,
					a = 8 * i - r - 1,
					u = (1 << a) - 1,
					c = u >> 1,
					l = -7,
					f = n ? i - 1 : 0,
					p = n ? -1 : 1,
					h = e[t + f];
				for (
					f += p, o = h & ((1 << -l) - 1), h >>= -l, l += a;
					l > 0;
					o = 256 * o + e[t + f], f += p, l -= 8
				);
				for (
					s = o & ((1 << -l) - 1), o >>= -l, l += r;
					l > 0;
					s = 256 * s + e[t + f], f += p, l -= 8
				);
				if (0 === o) o = 1 - c;
				else {
					if (o === u) return s ? NaN : (1 / 0) * (h ? -1 : 1);
					(s += Math.pow(2, r)), (o -= c);
				}
				return (h ? -1 : 1) * s * Math.pow(2, o - r);
			}),
				(t.write = function (e, t, n, r, i, o) {
					var s,
						a,
						u,
						c = 8 * o - i - 1,
						l = (1 << c) - 1,
						f = l >> 1,
						p = 23 === i ? Math.pow(2, -24) - Math.pow(2, -77) : 0,
						h = r ? 0 : o - 1,
						g = r ? 1 : -1,
						d = t < 0 || (0 === t && 1 / t < 0) ? 1 : 0;
					for (
						t = Math.abs(t),
							isNaN(t) || t === 1 / 0
								? ((a = isNaN(t) ? 1 : 0), (s = l))
								: ((s = Math.floor(Math.log(t) / Math.LN2)),
								  t * (u = Math.pow(2, -s)) < 1 && (s--, (u *= 2)),
								  (t += s + f >= 1 ? p / u : p * Math.pow(2, 1 - f)) * u >= 2 &&
										(s++, (u /= 2)),
								  s + f >= l
										? ((a = 0), (s = l))
										: s + f >= 1
										? ((a = (t * u - 1) * Math.pow(2, i)), (s += f))
										: ((a = t * Math.pow(2, f - 1) * Math.pow(2, i)), (s = 0)));
						i >= 8;
						e[n + h] = 255 & a, h += g, a /= 256, i -= 8
					);
					for (
						s = (s << i) | a, c += i;
						c > 0;
						e[n + h] = 255 & s, h += g, s /= 256, c -= 8
					);
					e[n + h - g] |= 128 * d;
				});
		},
		function (e, t) {
			var n = {}.toString;
			e.exports =
				Array.isArray ||
				function (e) {
					return "[object Array]" == n.call(e);
				};
		},
		function (e, t) {
			!(function (e) {
				"use strict";
				if (!e.fetch) {
					var t = "URLSearchParams" in e,
						n = "Symbol" in e && "iterator" in Symbol,
						r =
							"FileReader" in e &&
							"Blob" in e &&
							(function () {
								try {
									return new Blob(), !0;
								} catch (e) {
									return !1;
								}
							})(),
						i = "FormData" in e,
						o = "ArrayBuffer" in e;
					if (o)
						var s = [
								"[object Int8Array]",
								"[object Uint8Array]",
								"[object Uint8ClampedArray]",
								"[object Int16Array]",
								"[object Uint16Array]",
								"[object Int32Array]",
								"[object Uint32Array]",
								"[object Float32Array]",
								"[object Float64Array]",
							],
							a = function (e) {
								return e && DataView.prototype.isPrototypeOf(e);
							},
							u =
								ArrayBuffer.isView ||
								function (e) {
									return e && s.indexOf(Object.prototype.toString.call(e)) > -1;
								};
					(g.prototype.append = function (e, t) {
						(e = f(e)), (t = p(t));
						var n = this.map[e];
						this.map[e] = n ? n + "," + t : t;
					}),
						(g.prototype.delete = function (e) {
							delete this.map[f(e)];
						}),
						(g.prototype.get = function (e) {
							return (e = f(e)), this.has(e) ? this.map[e] : null;
						}),
						(g.prototype.has = function (e) {
							return this.map.hasOwnProperty(f(e));
						}),
						(g.prototype.set = function (e, t) {
							this.map[f(e)] = p(t);
						}),
						(g.prototype.forEach = function (e, t) {
							for (var n in this.map)
								this.map.hasOwnProperty(n) && e.call(t, this.map[n], n, this);
						}),
						(g.prototype.keys = function () {
							var e = [];
							return (
								this.forEach(function (t, n) {
									e.push(n);
								}),
								h(e)
							);
						}),
						(g.prototype.values = function () {
							var e = [];
							return (
								this.forEach(function (t) {
									e.push(t);
								}),
								h(e)
							);
						}),
						(g.prototype.entries = function () {
							var e = [];
							return (
								this.forEach(function (t, n) {
									e.push([n, t]);
								}),
								h(e)
							);
						}),
						n && (g.prototype[Symbol.iterator] = g.prototype.entries);
					var c = ["DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT"];
					(S.prototype.clone = function () {
						return new S(this, { body: this._bodyInit });
					}),
						w.call(S.prototype),
						w.call(v.prototype),
						(v.prototype.clone = function () {
							return new v(this._bodyInit, {
								status: this.status,
								statusText: this.statusText,
								headers: new g(this.headers),
								url: this.url,
							});
						}),
						(v.error = function () {
							var e = new v(null, { status: 0, statusText: "" });
							return (e.type = "error"), e;
						});
					var l = [301, 302, 303, 307, 308];
					(v.redirect = function (e, t) {
						if (-1 === l.indexOf(t))
							throw new RangeError("Invalid status code");
						return new v(null, { status: t, headers: { location: e } });
					}),
						(e.Headers = g),
						(e.Request = S),
						(e.Response = v),
						(e.fetch = function (e, t) {
							return new Promise(function (n, i) {
								var o = new S(e, t),
									s = new XMLHttpRequest();
								(s.onload = function () {
									var e,
										t,
										r = {
											status: s.status,
											statusText: s.statusText,
											headers:
												((e = s.getAllResponseHeaders() || ""),
												(t = new g()),
												e
													.replace(/\r?\n[\t ]+/g, " ")
													.split(/\r?\n/)
													.forEach(function (e) {
														var n = e.split(":"),
															r = n.shift().trim();
														if (r) {
															var i = n.join(":").trim();
															t.append(r, i);
														}
													}),
												t),
										};
									r.url =
										"responseURL" in s
											? s.responseURL
											: r.headers.get("X-Request-URL");
									var i = "response" in s ? s.response : s.responseText;
									n(new v(i, r));
								}),
									(s.onerror = function () {
										i(new TypeError("Network request failed"));
									}),
									(s.ontimeout = function () {
										i(new TypeError("Network request failed"));
									}),
									s.open(o.method, o.url, !0),
									"include" === o.credentials
										? (s.withCredentials = !0)
										: "omit" === o.credentials && (s.withCredentials = !1),
									"responseType" in s && r && (s.responseType = "blob"),
									o.headers.forEach(function (e, t) {
										s.setRequestHeader(t, e);
									}),
									s.send(void 0 === o._bodyInit ? null : o._bodyInit);
							});
						}),
						(e.fetch.polyfill = !0);
				}
				function f(e) {
					if (
						("string" != typeof e && (e = String(e)),
						/[^a-z0-9\-#$%&'*+.\^_`|~]/i.test(e))
					)
						throw new TypeError("Invalid character in header field name");
					return e.toLowerCase();
				}
				function p(e) {
					return "string" != typeof e && (e = String(e)), e;
				}
				function h(e) {
					var t = {
						next: function () {
							var t = e.shift();
							return { done: void 0 === t, value: t };
						},
					};
					return (
						n &&
							(t[Symbol.iterator] = function () {
								return t;
							}),
						t
					);
				}
				function g(e) {
					(this.map = {}),
						e instanceof g
							? e.forEach(function (e, t) {
									this.append(t, e);
							  }, this)
							: Array.isArray(e)
							? e.forEach(function (e) {
									this.append(e[0], e[1]);
							  }, this)
							: e &&
							  Object.getOwnPropertyNames(e).forEach(function (t) {
									this.append(t, e[t]);
							  }, this);
				}
				function d(e) {
					if (e.bodyUsed) return Promise.reject(new TypeError("Already read"));
					e.bodyUsed = !0;
				}
				function y(e) {
					return new Promise(function (t, n) {
						(e.onload = function () {
							t(e.result);
						}),
							(e.onerror = function () {
								n(e.error);
							});
					});
				}
				function m(e) {
					var t = new FileReader(),
						n = y(t);
					return t.readAsArrayBuffer(e), n;
				}
				function b(e) {
					if (e.slice) return e.slice(0);
					var t = new Uint8Array(e.byteLength);
					return t.set(new Uint8Array(e)), t.buffer;
				}
				function w() {
					return (
						(this.bodyUsed = !1),
						(this._initBody = function (e) {
							if (((this._bodyInit = e), e))
								if ("string" == typeof e) this._bodyText = e;
								else if (r && Blob.prototype.isPrototypeOf(e))
									this._bodyBlob = e;
								else if (i && FormData.prototype.isPrototypeOf(e))
									this._bodyFormData = e;
								else if (t && URLSearchParams.prototype.isPrototypeOf(e))
									this._bodyText = e.toString();
								else if (o && r && a(e))
									(this._bodyArrayBuffer = b(e.buffer)),
										(this._bodyInit = new Blob([this._bodyArrayBuffer]));
								else {
									if (!o || (!ArrayBuffer.prototype.isPrototypeOf(e) && !u(e)))
										throw new Error("unsupported BodyInit type");
									this._bodyArrayBuffer = b(e);
								}
							else this._bodyText = "";
							this.headers.get("content-type") ||
								("string" == typeof e
									? this.headers.set("content-type", "text/plain;charset=UTF-8")
									: this._bodyBlob && this._bodyBlob.type
									? this.headers.set("content-type", this._bodyBlob.type)
									: t &&
									  URLSearchParams.prototype.isPrototypeOf(e) &&
									  this.headers.set(
											"content-type",
											"application/x-www-form-urlencoded;charset=UTF-8"
									  ));
						}),
						r &&
							((this.blob = function () {
								var e = d(this);
								if (e) return e;
								if (this._bodyBlob) return Promise.resolve(this._bodyBlob);
								if (this._bodyArrayBuffer)
									return Promise.resolve(new Blob([this._bodyArrayBuffer]));
								if (this._bodyFormData)
									throw new Error("could not read FormData body as blob");
								return Promise.resolve(new Blob([this._bodyText]));
							}),
							(this.arrayBuffer = function () {
								return this._bodyArrayBuffer
									? d(this) || Promise.resolve(this._bodyArrayBuffer)
									: this.blob().then(m);
							})),
						(this.text = function () {
							var e,
								t,
								n,
								r = d(this);
							if (r) return r;
							if (this._bodyBlob)
								return (
									(e = this._bodyBlob),
									(t = new FileReader()),
									(n = y(t)),
									t.readAsText(e),
									n
								);
							if (this._bodyArrayBuffer)
								return Promise.resolve(
									(function (e) {
										for (
											var t = new Uint8Array(e), n = new Array(t.length), r = 0;
											r < t.length;
											r++
										)
											n[r] = String.fromCharCode(t[r]);
										return n.join("");
									})(this._bodyArrayBuffer)
								);
							if (this._bodyFormData)
								throw new Error("could not read FormData body as text");
							return Promise.resolve(this._bodyText);
						}),
						i &&
							(this.formData = function () {
								return this.text().then(P);
							}),
						(this.json = function () {
							return this.text().then(JSON.parse);
						}),
						this
					);
				}
				function S(e, t) {
					var n,
						r,
						i = (t = t || {}).body;
					if (e instanceof S) {
						if (e.bodyUsed) throw new TypeError("Already read");
						(this.url = e.url),
							(this.credentials = e.credentials),
							t.headers || (this.headers = new g(e.headers)),
							(this.method = e.method),
							(this.mode = e.mode),
							i ||
								null == e._bodyInit ||
								((i = e._bodyInit), (e.bodyUsed = !0));
					} else this.url = String(e);
					if (
						((this.credentials = t.credentials || this.credentials || "omit"),
						(!t.headers && this.headers) || (this.headers = new g(t.headers)),
						(this.method =
							((n = t.method || this.method || "GET"),
							(r = n.toUpperCase()),
							c.indexOf(r) > -1 ? r : n)),
						(this.mode = t.mode || this.mode || null),
						(this.referrer = null),
						("GET" === this.method || "HEAD" === this.method) && i)
					)
						throw new TypeError("Body not allowed for GET or HEAD requests");
					this._initBody(i);
				}
				function P(e) {
					var t = new FormData();
					return (
						e
							.trim()
							.split("&")
							.forEach(function (e) {
								if (e) {
									var n = e.split("="),
										r = n.shift().replace(/\+/g, " "),
										i = n.join("=").replace(/\+/g, " ");
									t.append(decodeURIComponent(r), decodeURIComponent(i));
								}
							}),
						t
					);
				}
				function v(e, t) {
					t || (t = {}),
						(this.type = "default"),
						(this.status = void 0 === t.status ? 200 : t.status),
						(this.ok = this.status >= 200 && this.status < 300),
						(this.statusText = "statusText" in t ? t.statusText : "OK"),
						(this.headers = new g(t.headers)),
						(this.url = t.url || ""),
						this._initBody(e);
				}
			})("undefined" != typeof self ? self : this);
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = n(12);
			t.canReportError = function (e) {
				for (; e; ) {
					var t = e,
						n = t.closed,
						i = t.destination,
						o = t.isStopped;
					if (n || o) return !1;
					e = i && i instanceof r.Subscriber ? i : null;
				}
				return !0;
			};
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.isArray =
					Array.isArray ||
					function (e) {
						return e && "number" == typeof e.length;
					});
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.isObject = function (e) {
					return null !== e && "object" == typeof e;
				});
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = (function () {
				function e(e) {
					return (
						Error.call(this),
						(this.message = e
							? e.length +
							  " errors occurred during unsubscription:\n" +
							  e
									.map(function (e, t) {
										return t + 1 + ") " + e.toString();
									})
									.join("\n  ")
							: ""),
						(this.name = "UnsubscriptionError"),
						(this.errors = e),
						this
					);
				}
				return (e.prototype = Object.create(Error.prototype)), e;
			})();
			t.UnsubscriptionError = r;
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = n(12),
				i = n(15),
				o = n(21);
			t.toSubscriber = function (e, t, n) {
				if (e) {
					if (e instanceof r.Subscriber) return e;
					if (e[i.rxSubscriber]) return e[i.rxSubscriber]();
				}
				return e || t || n
					? new r.Subscriber(e, t, n)
					: new r.Subscriber(o.empty);
			};
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.observable =
					("function" == typeof Symbol && Symbol.observable) || "@@observable");
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = n(52);
			function i(e) {
				return 0 === e.length
					? r.identity
					: 1 === e.length
					? e[0]
					: function (t) {
							return e.reduce(function (e, t) {
								return t(e);
							}, t);
					  };
			}
			(t.pipe = function () {
				for (var e = [], t = 0; t < arguments.length; t++) e[t] = arguments[t];
				return i(e);
			}),
				(t.pipeFromArray = i);
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 }),
				(t.identity = function (e) {
					return e;
				});
		},
		function (e, t, n) {
			"use strict";
			Object.defineProperty(t, "__esModule", { value: !0 });
			var r = (function () {
				function e() {
					return (
						Error.call(this),
						(this.message = "object unsubscribed"),
						(this.name = "ObjectUnsubscribedError"),
						this
					);
				}
				return (e.prototype = Object.create(Error.prototype)), e;
			})();
			t.ObjectUnsubscribedError = r;
		},
		function (e, t, n) {
			"use strict";
			var r,
				i =
					(this && this.__extends) ||
					((r = function (e, t) {
						return (r =
							Object.setPrototypeOf ||
							({ __proto__: [] } instanceof Array &&
								function (e, t) {
									e.__proto__ = t;
								}) ||
							function (e, t) {
								for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
							})(e, t);
					}),
					function (e, t) {
						function n() {
							this.constructor = e;
						}
						r(e, t),
							(e.prototype =
								null === t
									? Object.create(t)
									: ((n.prototype = t.prototype), new n()));
					});
			Object.defineProperty(t, "__esModule", { value: !0 });
			var o = (function (e) {
				function t(t, n) {
					var r = e.call(this) || this;
					return (r.subject = t), (r.subscriber = n), (r.closed = !1), r;
				}
				return (
					i(t, e),
					(t.prototype.unsubscribe = function () {
						if (!this.closed) {
							this.closed = !0;
							var e = this.subject,
								t = e.observers;
							if (
								((this.subject = null),
								t && 0 !== t.length && !e.isStopped && !e.closed)
							) {
								var n = t.indexOf(this.subscriber);
								-1 !== n && t.splice(n, 1);
							}
						}
					}),
					t
				);
			})(n(14).Subscription);
			t.SubjectSubscription = o;
		},
		function (e, t, n) {
			"use strict";
			n.r(t),
				n.d(t, "manager", function () {
					return ot.manager;
				}),
				n.d(t, "peers", function () {
					return Dt.peers;
				}),
				n.d(t, "EBLibrary", function () {
					return er;
				}),
				n.d(t, "VERSION", function () {
					return Zn;
				});
			/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
			var r = function (e, t) {
				return (r =
					Object.setPrototypeOf ||
					({ __proto__: [] } instanceof Array &&
						function (e, t) {
							e.__proto__ = t;
						}) ||
					function (e, t) {
						for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
					})(e, t);
			};
			function i(e, t) {
				function n() {
					this.constructor = e;
				}
				r(e, t),
					(e.prototype =
						null === t
							? Object.create(t)
							: ((n.prototype = t.prototype), new n()));
			}
			var o = function () {
				return (o =
					Object.assign ||
					function (e) {
						for (var t, n = 1, r = arguments.length; n < r; n++)
							for (var i in (t = arguments[n]))
								Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i]);
						return e;
					}).apply(this, arguments);
			};
			function s(e) {
				return "function" == typeof e;
			}
			var a = !1,
				u = {
					Promise: void 0,
					set useDeprecatedSynchronousErrorHandling(e) {
						e && new Error().stack;
						a = e;
					},
					get useDeprecatedSynchronousErrorHandling() {
						return a;
					},
				};
			function c(e) {
				setTimeout(function () {
					throw e;
				}, 0);
			}
			var l = {
					closed: !0,
					next: function (e) {},
					error: function (e) {
						if (u.useDeprecatedSynchronousErrorHandling) throw e;
						c(e);
					},
					complete: function () {},
				},
				f = (function () {
					return (
						Array.isArray ||
						function (e) {
							return e && "number" == typeof e.length;
						}
					);
				})();
			function p(e) {
				return null !== e && "object" == typeof e;
			}
			var h = (function () {
					function e(e) {
						return (
							Error.call(this),
							(this.message = e
								? e.length +
								  " errors occurred during unsubscription:\n" +
								  e
										.map(function (e, t) {
											return t + 1 + ") " + e.toString();
										})
										.join("\n  ")
								: ""),
							(this.name = "UnsubscriptionError"),
							(this.errors = e),
							this
						);
					}
					return (e.prototype = Object.create(Error.prototype)), e;
				})(),
				g = (function () {
					function e(e) {
						(this.closed = !1),
							(this._parentOrParents = null),
							(this._subscriptions = null),
							e && ((this._ctorUnsubscribe = !0), (this._unsubscribe = e));
					}
					return (
						(e.prototype.unsubscribe = function () {
							var t;
							if (!this.closed) {
								var n = this._parentOrParents,
									r = this._ctorUnsubscribe,
									i = this._unsubscribe,
									o = this._subscriptions;
								if (
									((this.closed = !0),
									(this._parentOrParents = null),
									(this._subscriptions = null),
									n instanceof e)
								)
									n.remove(this);
								else if (null !== n)
									for (var a = 0; a < n.length; ++a) {
										n[a].remove(this);
									}
								if (s(i)) {
									r && (this._unsubscribe = void 0);
									try {
										i.call(this);
									} catch (e) {
										t = e instanceof h ? d(e.errors) : [e];
									}
								}
								if (f(o)) {
									a = -1;
									for (var u = o.length; ++a < u; ) {
										var c = o[a];
										if (p(c))
											try {
												c.unsubscribe();
											} catch (e) {
												(t = t || []),
													e instanceof h
														? (t = t.concat(d(e.errors)))
														: t.push(e);
											}
									}
								}
								if (t) throw new h(t);
							}
						}),
						(e.prototype.add = function (t) {
							var n = t;
							if (!t) return e.EMPTY;
							switch (typeof t) {
								case "function":
									n = new e(t);
								case "object":
									if (
										n === this ||
										n.closed ||
										"function" != typeof n.unsubscribe
									)
										return n;
									if (this.closed) return n.unsubscribe(), n;
									if (!(n instanceof e)) {
										var r = n;
										(n = new e())._subscriptions = [r];
									}
									break;
								default:
									throw new Error(
										"unrecognized teardown " + t + " added to Subscription."
									);
							}
							var i = n._parentOrParents;
							if (null === i) n._parentOrParents = this;
							else if (i instanceof e) {
								if (i === this) return n;
								n._parentOrParents = [i, this];
							} else {
								if (-1 !== i.indexOf(this)) return n;
								i.push(this);
							}
							var o = this._subscriptions;
							return null === o ? (this._subscriptions = [n]) : o.push(n), n;
						}),
						(e.prototype.remove = function (e) {
							var t = this._subscriptions;
							if (t) {
								var n = t.indexOf(e);
								-1 !== n && t.splice(n, 1);
							}
						}),
						(e.EMPTY = (function (e) {
							return (e.closed = !0), e;
						})(new e())),
						e
					);
				})();
			function d(e) {
				return e.reduce(function (e, t) {
					return e.concat(t instanceof h ? t.errors : t);
				}, []);
			}
			var y = (function () {
					return "function" == typeof Symbol
						? Symbol("rxSubscriber")
						: "@@rxSubscriber_" + Math.random();
				})(),
				m = (function (e) {
					function t(n, r, i) {
						var o = e.call(this) || this;
						switch (
							((o.syncErrorValue = null),
							(o.syncErrorThrown = !1),
							(o.syncErrorThrowable = !1),
							(o.isStopped = !1),
							arguments.length)
						) {
							case 0:
								o.destination = l;
								break;
							case 1:
								if (!n) {
									o.destination = l;
									break;
								}
								if ("object" == typeof n) {
									n instanceof t
										? ((o.syncErrorThrowable = n.syncErrorThrowable),
										  (o.destination = n),
										  n.add(o))
										: ((o.syncErrorThrowable = !0),
										  (o.destination = new b(o, n)));
									break;
								}
							default:
								(o.syncErrorThrowable = !0),
									(o.destination = new b(o, n, r, i));
						}
						return o;
					}
					return (
						i(t, e),
						(t.prototype[y] = function () {
							return this;
						}),
						(t.create = function (e, n, r) {
							var i = new t(e, n, r);
							return (i.syncErrorThrowable = !1), i;
						}),
						(t.prototype.next = function (e) {
							this.isStopped || this._next(e);
						}),
						(t.prototype.error = function (e) {
							this.isStopped || ((this.isStopped = !0), this._error(e));
						}),
						(t.prototype.complete = function () {
							this.isStopped || ((this.isStopped = !0), this._complete());
						}),
						(t.prototype.unsubscribe = function () {
							this.closed ||
								((this.isStopped = !0), e.prototype.unsubscribe.call(this));
						}),
						(t.prototype._next = function (e) {
							this.destination.next(e);
						}),
						(t.prototype._error = function (e) {
							this.destination.error(e), this.unsubscribe();
						}),
						(t.prototype._complete = function () {
							this.destination.complete(), this.unsubscribe();
						}),
						(t.prototype._unsubscribeAndRecycle = function () {
							var e = this._parentOrParents;
							return (
								(this._parentOrParents = null),
								this.unsubscribe(),
								(this.closed = !1),
								(this.isStopped = !1),
								(this._parentOrParents = e),
								this
							);
						}),
						t
					);
				})(g),
				b = (function (e) {
					function t(t, n, r, i) {
						var o,
							a = e.call(this) || this;
						a._parentSubscriber = t;
						var u = a;
						return (
							s(n)
								? (o = n)
								: n &&
								  ((o = n.next),
								  (r = n.error),
								  (i = n.complete),
								  n !== l &&
										(s((u = Object.create(n)).unsubscribe) &&
											a.add(u.unsubscribe.bind(u)),
										(u.unsubscribe = a.unsubscribe.bind(a)))),
							(a._context = u),
							(a._next = o),
							(a._error = r),
							(a._complete = i),
							a
						);
					}
					return (
						i(t, e),
						(t.prototype.next = function (e) {
							if (!this.isStopped && this._next) {
								var t = this._parentSubscriber;
								u.useDeprecatedSynchronousErrorHandling && t.syncErrorThrowable
									? this.__tryOrSetError(t, this._next, e) && this.unsubscribe()
									: this.__tryOrUnsub(this._next, e);
							}
						}),
						(t.prototype.error = function (e) {
							if (!this.isStopped) {
								var t = this._parentSubscriber,
									n = u.useDeprecatedSynchronousErrorHandling;
								if (this._error)
									n && t.syncErrorThrowable
										? (this.__tryOrSetError(t, this._error, e),
										  this.unsubscribe())
										: (this.__tryOrUnsub(this._error, e), this.unsubscribe());
								else if (t.syncErrorThrowable)
									n ? ((t.syncErrorValue = e), (t.syncErrorThrown = !0)) : c(e),
										this.unsubscribe();
								else {
									if ((this.unsubscribe(), n)) throw e;
									c(e);
								}
							}
						}),
						(t.prototype.complete = function () {
							var e = this;
							if (!this.isStopped) {
								var t = this._parentSubscriber;
								if (this._complete) {
									var n = function () {
										return e._complete.call(e._context);
									};
									u.useDeprecatedSynchronousErrorHandling &&
									t.syncErrorThrowable
										? (this.__tryOrSetError(t, n), this.unsubscribe())
										: (this.__tryOrUnsub(n), this.unsubscribe());
								} else this.unsubscribe();
							}
						}),
						(t.prototype.__tryOrUnsub = function (e, t) {
							try {
								e.call(this._context, t);
							} catch (e) {
								if (
									(this.unsubscribe(), u.useDeprecatedSynchronousErrorHandling)
								)
									throw e;
								c(e);
							}
						}),
						(t.prototype.__tryOrSetError = function (e, t, n) {
							if (!u.useDeprecatedSynchronousErrorHandling)
								throw new Error("bad call");
							try {
								t.call(this._context, n);
							} catch (t) {
								return u.useDeprecatedSynchronousErrorHandling
									? ((e.syncErrorValue = t), (e.syncErrorThrown = !0), !0)
									: (c(t), !0);
							}
							return !1;
						}),
						(t.prototype._unsubscribe = function () {
							var e = this._parentSubscriber;
							(this._context = null),
								(this._parentSubscriber = null),
								e.unsubscribe();
						}),
						t
					);
				})(m);
			var w = (function () {
				return (
					("function" == typeof Symbol && Symbol.observable) || "@@observable"
				);
			})();
			function S(e) {
				return e;
			}
			function P() {
				for (var e = [], t = 0; t < arguments.length; t++) e[t] = arguments[t];
				return v(e);
			}
			function v(e) {
				return 0 === e.length
					? S
					: 1 === e.length
					? e[0]
					: function (t) {
							return e.reduce(function (e, t) {
								return t(e);
							}, t);
					  };
			}
			var A = (function () {
				function e(e) {
					(this._isScalar = !1), e && (this._subscribe = e);
				}
				return (
					(e.prototype.lift = function (t) {
						var n = new e();
						return (n.source = this), (n.operator = t), n;
					}),
					(e.prototype.subscribe = function (e, t, n) {
						var r = this.operator,
							i = (function (e, t, n) {
								if (e) {
									if (e instanceof m) return e;
									if (e[y]) return e[y]();
								}
								return e || t || n ? new m(e, t, n) : new m(l);
							})(e, t, n);
						if (
							(r
								? i.add(r.call(i, this.source))
								: i.add(
										this.source ||
											(u.useDeprecatedSynchronousErrorHandling &&
												!i.syncErrorThrowable)
											? this._subscribe(i)
											: this._trySubscribe(i)
								  ),
							u.useDeprecatedSynchronousErrorHandling &&
								i.syncErrorThrowable &&
								((i.syncErrorThrowable = !1), i.syncErrorThrown))
						)
							throw i.syncErrorValue;
						return i;
					}),
					(e.prototype._trySubscribe = function (e) {
						try {
							return this._subscribe(e);
						} catch (t) {
							u.useDeprecatedSynchronousErrorHandling &&
								((e.syncErrorThrown = !0), (e.syncErrorValue = t)),
								!(function (e) {
									for (; e; ) {
										var t = e,
											n = t.closed,
											r = t.destination,
											i = t.isStopped;
										if (n || i) return !1;
										e = r && r instanceof m ? r : null;
									}
									return !0;
								})(e)
									? console.warn(t)
									: e.error(t);
						}
					}),
					(e.prototype.forEach = function (e, t) {
						var n = this;
						return new (t = O(t))(function (t, r) {
							var i;
							i = n.subscribe(
								function (t) {
									try {
										e(t);
									} catch (e) {
										r(e), i && i.unsubscribe();
									}
								},
								r,
								t
							);
						});
					}),
					(e.prototype._subscribe = function (e) {
						var t = this.source;
						return t && t.subscribe(e);
					}),
					(e.prototype[w] = function () {
						return this;
					}),
					(e.prototype.pipe = function () {
						for (var e = [], t = 0; t < arguments.length; t++)
							e[t] = arguments[t];
						return 0 === e.length ? this : v(e)(this);
					}),
					(e.prototype.toPromise = function (e) {
						var t = this;
						return new (e = O(e))(function (e, n) {
							var r;
							t.subscribe(
								function (e) {
									return (r = e);
								},
								function (e) {
									return n(e);
								},
								function () {
									return e(r);
								}
							);
						});
					}),
					(e.create = function (t) {
						return new e(t);
					}),
					e
				);
			})();
			function O(e) {
				if ((e || (e = u.Promise || Promise), !e))
					throw new Error("no Promise impl found");
				return e;
			}
			var T = (function () {
					function e() {
						return (
							Error.call(this),
							(this.message = "object unsubscribed"),
							(this.name = "ObjectUnsubscribedError"),
							this
						);
					}
					return (e.prototype = Object.create(Error.prototype)), e;
				})(),
				C = (function (e) {
					function t(t, n) {
						var r = e.call(this) || this;
						return (r.subject = t), (r.subscriber = n), (r.closed = !1), r;
					}
					return (
						i(t, e),
						(t.prototype.unsubscribe = function () {
							if (!this.closed) {
								this.closed = !0;
								var e = this.subject,
									t = e.observers;
								if (
									((this.subject = null),
									t && 0 !== t.length && !e.isStopped && !e.closed)
								) {
									var n = t.indexOf(this.subscriber);
									-1 !== n && t.splice(n, 1);
								}
							}
						}),
						t
					);
				})(g),
				R = (function (e) {
					function t(t) {
						var n = e.call(this, t) || this;
						return (n.destination = t), n;
					}
					return i(t, e), t;
				})(m),
				E = (function (e) {
					function t() {
						var t = e.call(this) || this;
						return (
							(t.observers = []),
							(t.closed = !1),
							(t.isStopped = !1),
							(t.hasError = !1),
							(t.thrownError = null),
							t
						);
					}
					return (
						i(t, e),
						(t.prototype[y] = function () {
							return new R(this);
						}),
						(t.prototype.lift = function (e) {
							var t = new M(this, this);
							return (t.operator = e), t;
						}),
						(t.prototype.next = function (e) {
							if (this.closed) throw new T();
							if (!this.isStopped)
								for (
									var t = this.observers, n = t.length, r = t.slice(), i = 0;
									i < n;
									i++
								)
									r[i].next(e);
						}),
						(t.prototype.error = function (e) {
							if (this.closed) throw new T();
							(this.hasError = !0),
								(this.thrownError = e),
								(this.isStopped = !0);
							for (
								var t = this.observers, n = t.length, r = t.slice(), i = 0;
								i < n;
								i++
							)
								r[i].error(e);
							this.observers.length = 0;
						}),
						(t.prototype.complete = function () {
							if (this.closed) throw new T();
							this.isStopped = !0;
							for (
								var e = this.observers, t = e.length, n = e.slice(), r = 0;
								r < t;
								r++
							)
								n[r].complete();
							this.observers.length = 0;
						}),
						(t.prototype.unsubscribe = function () {
							(this.isStopped = !0),
								(this.closed = !0),
								(this.observers = null);
						}),
						(t.prototype._trySubscribe = function (t) {
							if (this.closed) throw new T();
							return e.prototype._trySubscribe.call(this, t);
						}),
						(t.prototype._subscribe = function (e) {
							if (this.closed) throw new T();
							return this.hasError
								? (e.error(this.thrownError), g.EMPTY)
								: this.isStopped
								? (e.complete(), g.EMPTY)
								: (this.observers.push(e), new C(this, e));
						}),
						(t.prototype.asObservable = function () {
							var e = new A();
							return (e.source = this), e;
						}),
						(t.create = function (e, t) {
							return new M(e, t);
						}),
						t
					);
				})(A),
				M = (function (e) {
					function t(t, n) {
						var r = e.call(this) || this;
						return (r.destination = t), (r.source = n), r;
					}
					return (
						i(t, e),
						(t.prototype.next = function (e) {
							var t = this.destination;
							t && t.next && t.next(e);
						}),
						(t.prototype.error = function (e) {
							var t = this.destination;
							t && t.error && this.destination.error(e);
						}),
						(t.prototype.complete = function () {
							var e = this.destination;
							e && e.complete && this.destination.complete();
						}),
						(t.prototype._subscribe = function (e) {
							return this.source ? this.source.subscribe(e) : g.EMPTY;
						}),
						t
					);
				})(E);
			var L = (function () {
					function e(e, t, n, r) {
						(this.keySelector = e),
							(this.elementSelector = t),
							(this.durationSelector = n),
							(this.subjectSelector = r);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(
								new x(
									e,
									this.keySelector,
									this.elementSelector,
									this.durationSelector,
									this.subjectSelector
								)
							);
						}),
						e
					);
				})(),
				x = (function (e) {
					function t(t, n, r, i, o) {
						var s = e.call(this, t) || this;
						return (
							(s.keySelector = n),
							(s.elementSelector = r),
							(s.durationSelector = i),
							(s.subjectSelector = o),
							(s.groups = null),
							(s.attemptedToUnsubscribe = !1),
							(s.count = 0),
							s
						);
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							var t;
							try {
								t = this.keySelector(e);
							} catch (e) {
								return void this.error(e);
							}
							this._group(e, t);
						}),
						(t.prototype._group = function (e, t) {
							var n = this.groups;
							n || (n = this.groups = new Map());
							var r,
								i = n.get(t);
							if (this.elementSelector)
								try {
									r = this.elementSelector(e);
								} catch (e) {
									this.error(e);
								}
							else r = e;
							if (!i) {
								(i = this.subjectSelector ? this.subjectSelector() : new E()),
									n.set(t, i);
								var o = new I(t, i, this);
								if ((this.destination.next(o), this.durationSelector)) {
									var s = void 0;
									try {
										s = this.durationSelector(new I(t, i));
									} catch (e) {
										return void this.error(e);
									}
									this.add(s.subscribe(new D(t, i, this)));
								}
							}
							i.closed || i.next(r);
						}),
						(t.prototype._error = function (e) {
							var t = this.groups;
							t &&
								(t.forEach(function (t, n) {
									t.error(e);
								}),
								t.clear()),
								this.destination.error(e);
						}),
						(t.prototype._complete = function () {
							var e = this.groups;
							e &&
								(e.forEach(function (e, t) {
									e.complete();
								}),
								e.clear()),
								this.destination.complete();
						}),
						(t.prototype.removeGroup = function (e) {
							this.groups.delete(e);
						}),
						(t.prototype.unsubscribe = function () {
							this.closed ||
								((this.attemptedToUnsubscribe = !0),
								0 === this.count && e.prototype.unsubscribe.call(this));
						}),
						t
					);
				})(m),
				D = (function (e) {
					function t(t, n, r) {
						var i = e.call(this, n) || this;
						return (i.key = t), (i.group = n), (i.parent = r), i;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							this.complete();
						}),
						(t.prototype._unsubscribe = function () {
							var e = this.parent,
								t = this.key;
							(this.key = this.parent = null), e && e.removeGroup(t);
						}),
						t
					);
				})(m),
				I = (function (e) {
					function t(t, n, r) {
						var i = e.call(this) || this;
						return (
							(i.key = t), (i.groupSubject = n), (i.refCountSubscription = r), i
						);
					}
					return (
						i(t, e),
						(t.prototype._subscribe = function (e) {
							var t = new g(),
								n = this.refCountSubscription,
								r = this.groupSubject;
							return (
								n && !n.closed && t.add(new k(n)), t.add(r.subscribe(e)), t
							);
						}),
						t
					);
				})(A),
				k = (function (e) {
					function t(t) {
						var n = e.call(this) || this;
						return (n.parent = t), t.count++, n;
					}
					return (
						i(t, e),
						(t.prototype.unsubscribe = function () {
							var t = this.parent;
							t.closed ||
								this.closed ||
								(e.prototype.unsubscribe.call(this),
								(t.count -= 1),
								0 === t.count && t.attemptedToUnsubscribe && t.unsubscribe());
						}),
						t
					);
				})(g);
			function j(e, t) {
				return function (n) {
					if ("function" != typeof e)
						throw new TypeError(
							"argument is not a function. Are you looking for `mapTo()`?"
						);
					return n.lift(new B(e, t));
				};
			}
			var B = (function () {
					function e(e, t) {
						(this.project = e), (this.thisArg = t);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new N(e, this.project, this.thisArg));
						}),
						e
					);
				})(),
				N = (function (e) {
					function t(t, n, r) {
						var i = e.call(this, t) || this;
						return (i.project = n), (i.count = 0), (i.thisArg = r || i), i;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							var t;
							try {
								t = this.project.call(this.thisArg, e, this.count++);
							} catch (e) {
								return void this.destination.error(e);
							}
							this.destination.next(t);
						}),
						t
					);
				})(m),
				U = function (e) {
					return function (t) {
						for (var n = 0, r = e.length; n < r && !t.closed; n++) t.next(e[n]);
						t.complete();
					};
				};
			function _() {
				return "function" == typeof Symbol && Symbol.iterator
					? Symbol.iterator
					: "@@iterator";
			}
			var q = _(),
				V = function (e) {
					return e && "number" == typeof e.length && "function" != typeof e;
				};
			function F(e) {
				return (
					!!e && "function" != typeof e.subscribe && "function" == typeof e.then
				);
			}
			var z = function (e) {
				if (e && "function" == typeof e[w])
					return (
						(r = e),
						function (e) {
							var t = r[w]();
							if ("function" != typeof t.subscribe)
								throw new TypeError(
									"Provided object does not correctly implement Symbol.observable"
								);
							return t.subscribe(e);
						}
					);
				if (V(e)) return U(e);
				if (F(e))
					return (
						(n = e),
						function (e) {
							return (
								n
									.then(
										function (t) {
											e.closed || (e.next(t), e.complete());
										},
										function (t) {
											return e.error(t);
										}
									)
									.then(null, c),
								e
							);
						}
					);
				if (e && "function" == typeof e[q])
					return (
						(t = e),
						function (e) {
							for (var n = t[q](); ; ) {
								var r = void 0;
								try {
									r = n.next();
								} catch (t) {
									return e.error(t), e;
								}
								if (r.done) {
									e.complete();
									break;
								}
								if ((e.next(r.value), e.closed)) break;
							}
							return (
								"function" == typeof n.return &&
									e.add(function () {
										n.return && n.return();
									}),
								e
							);
						}
					);
				var t,
					n,
					r,
					i = p(e) ? "an invalid object" : "'" + e + "'";
				throw new TypeError(
					"You provided " +
						i +
						" where a stream was expected. You can provide an Observable, Promise, Array, or Iterable."
				);
			};
			function W(e, t) {
				return new A(function (n) {
					var r = new g(),
						i = 0;
					return (
						r.add(
							t.schedule(function () {
								i !== e.length
									? (n.next(e[i++]), n.closed || r.add(this.schedule()))
									: n.complete();
							})
						),
						r
					);
				});
			}
			function H(e, t) {
				if (null != e) {
					if (
						(function (e) {
							return e && "function" == typeof e[w];
						})(e)
					)
						return (function (e, t) {
							return new A(function (n) {
								var r = new g();
								return (
									r.add(
										t.schedule(function () {
											var i = e[w]();
											r.add(
												i.subscribe({
													next: function (e) {
														r.add(
															t.schedule(function () {
																return n.next(e);
															})
														);
													},
													error: function (e) {
														r.add(
															t.schedule(function () {
																return n.error(e);
															})
														);
													},
													complete: function () {
														r.add(
															t.schedule(function () {
																return n.complete();
															})
														);
													},
												})
											);
										})
									),
									r
								);
							});
						})(e, t);
					if (F(e))
						return (function (e, t) {
							return new A(function (n) {
								var r = new g();
								return (
									r.add(
										t.schedule(function () {
											return e.then(
												function (e) {
													r.add(
														t.schedule(function () {
															n.next(e),
																r.add(
																	t.schedule(function () {
																		return n.complete();
																	})
																);
														})
													);
												},
												function (e) {
													r.add(
														t.schedule(function () {
															return n.error(e);
														})
													);
												}
											);
										})
									),
									r
								);
							});
						})(e, t);
					if (V(e)) return W(e, t);
					if (
						(function (e) {
							return e && "function" == typeof e[q];
						})(e) ||
						"string" == typeof e
					)
						return (function (e, t) {
							if (!e) throw new Error("Iterable cannot be null");
							return new A(function (n) {
								var r,
									i = new g();
								return (
									i.add(function () {
										r && "function" == typeof r.return && r.return();
									}),
									i.add(
										t.schedule(function () {
											(r = e[q]()),
												i.add(
													t.schedule(function () {
														if (!n.closed) {
															var e, t;
															try {
																var i = r.next();
																(e = i.value), (t = i.done);
															} catch (e) {
																return void n.error(e);
															}
															t ? n.complete() : (n.next(e), this.schedule());
														}
													})
												);
										})
									),
									i
								);
							});
						})(e, t);
				}
				throw new TypeError(
					((null !== e && typeof e) || e) + " is not observable"
				);
			}
			function G(e, t) {
				return t ? H(e, t) : e instanceof A ? e : new A(z(e));
			}
			var Q = (function (e) {
					function t(t) {
						var n = e.call(this) || this;
						return (n.parent = t), n;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							this.parent.notifyNext(e);
						}),
						(t.prototype._error = function (e) {
							this.parent.notifyError(e), this.unsubscribe();
						}),
						(t.prototype._complete = function () {
							this.parent.notifyComplete(), this.unsubscribe();
						}),
						t
					);
				})(m),
				J = (function (e) {
					function t() {
						return (null !== e && e.apply(this, arguments)) || this;
					}
					return (
						i(t, e),
						(t.prototype.notifyNext = function (e) {
							this.destination.next(e);
						}),
						(t.prototype.notifyError = function (e) {
							this.destination.error(e);
						}),
						(t.prototype.notifyComplete = function () {
							this.destination.complete();
						}),
						t
					);
				})(m);
			function Y(e, t) {
				if (!t.closed) {
					if (e instanceof A) return e.subscribe(t);
					var n;
					try {
						n = z(e)(t);
					} catch (e) {
						t.error(e);
					}
					return n;
				}
			}
			function K(e, t, n) {
				return (
					void 0 === n && (n = Number.POSITIVE_INFINITY),
					"function" == typeof t
						? function (r) {
								return r.pipe(
									K(function (n, r) {
										return G(e(n, r)).pipe(
											j(function (e, i) {
												return t(n, e, r, i);
											})
										);
									}, n)
								);
						  }
						: ("number" == typeof t && (n = t),
						  function (t) {
								return t.lift(new X(e, n));
						  })
				);
			}
			var X = (function () {
					function e(e, t) {
						void 0 === t && (t = Number.POSITIVE_INFINITY),
							(this.project = e),
							(this.concurrent = t);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new $(e, this.project, this.concurrent));
						}),
						e
					);
				})(),
				$ = (function (e) {
					function t(t, n, r) {
						void 0 === r && (r = Number.POSITIVE_INFINITY);
						var i = e.call(this, t) || this;
						return (
							(i.project = n),
							(i.concurrent = r),
							(i.hasCompleted = !1),
							(i.buffer = []),
							(i.active = 0),
							(i.index = 0),
							i
						);
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							this.active < this.concurrent
								? this._tryNext(e)
								: this.buffer.push(e);
						}),
						(t.prototype._tryNext = function (e) {
							var t,
								n = this.index++;
							try {
								t = this.project(e, n);
							} catch (e) {
								return void this.destination.error(e);
							}
							this.active++, this._innerSub(t);
						}),
						(t.prototype._innerSub = function (e) {
							var t = new Q(this),
								n = this.destination;
							n.add(t);
							var r = Y(e, t);
							r !== t && n.add(r);
						}),
						(t.prototype._complete = function () {
							(this.hasCompleted = !0),
								0 === this.active &&
									0 === this.buffer.length &&
									this.destination.complete(),
								this.unsubscribe();
						}),
						(t.prototype.notifyNext = function (e) {
							this.destination.next(e);
						}),
						(t.prototype.notifyComplete = function () {
							var e = this.buffer;
							this.active--,
								e.length > 0
									? this._next(e.shift())
									: 0 === this.active &&
									  this.hasCompleted &&
									  this.destination.complete();
						}),
						t
					);
				})(J),
				Z = (function (e) {
					function t(t, n) {
						var r = e.call(this, t, n) || this;
						return (r.scheduler = t), (r.work = n), (r.pending = !1), r;
					}
					return (
						i(t, e),
						(t.prototype.schedule = function (e, t) {
							if ((void 0 === t && (t = 0), this.closed)) return this;
							this.state = e;
							var n = this.id,
								r = this.scheduler;
							return (
								null != n && (this.id = this.recycleAsyncId(r, n, t)),
								(this.pending = !0),
								(this.delay = t),
								(this.id = this.id || this.requestAsyncId(r, this.id, t)),
								this
							);
						}),
						(t.prototype.requestAsyncId = function (e, t, n) {
							return (
								void 0 === n && (n = 0), setInterval(e.flush.bind(e, this), n)
							);
						}),
						(t.prototype.recycleAsyncId = function (e, t, n) {
							if (
								(void 0 === n && (n = 0),
								null !== n && this.delay === n && !1 === this.pending)
							)
								return t;
							clearInterval(t);
						}),
						(t.prototype.execute = function (e, t) {
							if (this.closed) return new Error("executing a cancelled action");
							this.pending = !1;
							var n = this._execute(e, t);
							if (n) return n;
							!1 === this.pending &&
								null != this.id &&
								(this.id = this.recycleAsyncId(this.scheduler, this.id, null));
						}),
						(t.prototype._execute = function (e, t) {
							var n = !1,
								r = void 0;
							try {
								this.work(e);
							} catch (e) {
								(n = !0), (r = (!!e && e) || new Error(e));
							}
							if (n) return this.unsubscribe(), r;
						}),
						(t.prototype._unsubscribe = function () {
							var e = this.id,
								t = this.scheduler,
								n = t.actions,
								r = n.indexOf(this);
							(this.work = null),
								(this.state = null),
								(this.pending = !1),
								(this.scheduler = null),
								-1 !== r && n.splice(r, 1),
								null != e && (this.id = this.recycleAsyncId(t, e, null)),
								(this.delay = null);
						}),
						t
					);
				})(
					(function (e) {
						function t(t, n) {
							return e.call(this) || this;
						}
						return (
							i(t, e),
							(t.prototype.schedule = function (e, t) {
								return void 0 === t && (t = 0), this;
							}),
							t
						);
					})(g)
				),
				ee = (function () {
					function e(t, n) {
						void 0 === n && (n = e.now),
							(this.SchedulerAction = t),
							(this.now = n);
					}
					return (
						(e.prototype.schedule = function (e, t, n) {
							return (
								void 0 === t && (t = 0),
								new this.SchedulerAction(this, e).schedule(n, t)
							);
						}),
						(e.now = function () {
							return Date.now();
						}),
						e
					);
				})(),
				te = (function (e) {
					function t(n, r) {
						void 0 === r && (r = ee.now);
						var i =
							e.call(this, n, function () {
								return t.delegate && t.delegate !== i ? t.delegate.now() : r();
							}) || this;
						return (i.actions = []), (i.active = !1), (i.scheduled = void 0), i;
					}
					return (
						i(t, e),
						(t.prototype.schedule = function (n, r, i) {
							return (
								void 0 === r && (r = 0),
								t.delegate && t.delegate !== this
									? t.delegate.schedule(n, r, i)
									: e.prototype.schedule.call(this, n, r, i)
							);
						}),
						(t.prototype.flush = function (e) {
							var t = this.actions;
							if (this.active) t.push(e);
							else {
								var n;
								this.active = !0;
								do {
									if ((n = e.execute(e.state, e.delay))) break;
								} while ((e = t.shift()));
								if (((this.active = !1), n)) {
									for (; (e = t.shift()); ) e.unsubscribe();
									throw n;
								}
							}
						}),
						t
					);
				})(ee),
				ne = new te(Z),
				re = { leading: !0, trailing: !1 };
			var ie = (function () {
					function e(e, t, n, r) {
						(this.duration = e),
							(this.scheduler = t),
							(this.leading = n),
							(this.trailing = r);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(
								new oe(
									e,
									this.duration,
									this.scheduler,
									this.leading,
									this.trailing
								)
							);
						}),
						e
					);
				})(),
				oe = (function (e) {
					function t(t, n, r, i, o) {
						var s = e.call(this, t) || this;
						return (
							(s.duration = n),
							(s.scheduler = r),
							(s.leading = i),
							(s.trailing = o),
							(s._hasTrailingValue = !1),
							(s._trailingValue = null),
							s
						);
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							this.throttled
								? this.trailing &&
								  ((this._trailingValue = e), (this._hasTrailingValue = !0))
								: (this.add(
										(this.throttled = this.scheduler.schedule(
											se,
											this.duration,
											{ subscriber: this }
										))
								  ),
								  this.leading
										? this.destination.next(e)
										: this.trailing &&
										  ((this._trailingValue = e),
										  (this._hasTrailingValue = !0)));
						}),
						(t.prototype._complete = function () {
							this._hasTrailingValue
								? (this.destination.next(this._trailingValue),
								  this.destination.complete())
								: this.destination.complete();
						}),
						(t.prototype.clearThrottle = function () {
							var e = this.throttled;
							e &&
								(this.trailing &&
									this._hasTrailingValue &&
									(this.destination.next(this._trailingValue),
									(this._trailingValue = null),
									(this._hasTrailingValue = !1)),
								e.unsubscribe(),
								this.remove(e),
								(this.throttled = null));
						}),
						t
					);
				})(m);
			function se(e) {
				e.subscriber.clearThrottle();
			}
			var ae = n(9);
			function ue(e, t, n, r) {
				return (
					s(n) && ((r = n), (n = void 0)),
					r
						? ue(e, t, n).pipe(
								j(function (e) {
									return f(e) ? r.apply(void 0, e) : r(e);
								})
						  )
						: new A(function (r) {
								!(function e(t, n, r, i, o) {
									var s;
									if (
										(function (e) {
											return (
												e &&
												"function" == typeof e.addEventListener &&
												"function" == typeof e.removeEventListener
											);
										})(t)
									) {
										var a = t;
										t.addEventListener(n, r, o),
											(s = function () {
												return a.removeEventListener(n, r, o);
											});
									} else if (
										(function (e) {
											return (
												e &&
												"function" == typeof e.on &&
												"function" == typeof e.off
											);
										})(t)
									) {
										var u = t;
										t.on(n, r),
											(s = function () {
												return u.off(n, r);
											});
									} else if (
										(function (e) {
											return (
												e &&
												"function" == typeof e.addListener &&
												"function" == typeof e.removeListener
											);
										})(t)
									) {
										var c = t;
										t.addListener(n, r),
											(s = function () {
												return c.removeListener(n, r);
											});
									} else {
										if (!t || !t.length)
											throw new TypeError("Invalid event target");
										for (var l = 0, f = t.length; l < f; l++)
											e(t[l], n, r, i, o);
									}
									i.add(s);
								})(
									e,
									t,
									function (e) {
										arguments.length > 1
											? r.next(Array.prototype.slice.call(arguments))
											: r.next(e);
									},
									r,
									n
								);
						  })
				);
			}
			function ce(e, t) {
				var n;
				return (
					void 0 === e && (e = 0),
					void 0 === t && (t = ne),
					(f((n = e)) || !(n - parseFloat(n) + 1 >= 0) || e < 0) && (e = 0),
					(t && "function" == typeof t.schedule) || (t = ne),
					new A(function (n) {
						return (
							n.add(
								t.schedule(le, e, { subscriber: n, counter: 0, period: e })
							),
							n
						);
					})
				);
			}
			function le(e) {
				var t = e.subscriber,
					n = e.counter,
					r = e.period;
				t.next(n),
					this.schedule({ subscriber: t, counter: n + 1, period: r }, r);
			}
			function fe(e) {
				return function (t) {
					return t.lift(new pe(e));
				};
			}
			var pe = (function () {
					function e(e) {
						this.value = e;
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new he(e, this.value));
						}),
						e
					);
				})(),
				he = (function (e) {
					function t(t, n) {
						var r = e.call(this, t) || this;
						return (r.value = n), r;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							this.destination.next(this.value);
						}),
						t
					);
				})(m);
			function ge(e) {
				return e && "function" == typeof e.schedule;
			}
			function de(e) {
				return void 0 === e && (e = Number.POSITIVE_INFINITY), K(S, e);
			}
			function ye(e, t) {
				return t ? W(e, t) : new A(U(e));
			}
			function me() {
				for (var e = [], t = 0; t < arguments.length; t++) e[t] = arguments[t];
				var n = Number.POSITIVE_INFINITY,
					r = null,
					i = e[e.length - 1];
				return (
					ge(i)
						? ((r = e.pop()),
						  e.length > 1 &&
								"number" == typeof e[e.length - 1] &&
								(n = e.pop()))
						: "number" == typeof i && (n = e.pop()),
					null === r && 1 === e.length && e[0] instanceof A
						? e[0]
						: de(n)(ye(e, r))
				);
			}
			var be = function (e) {
					return new ot.manager.PlayerEvent({
						Type: "register",
						Codec: "-",
						TimeShift: 0,
						Quality: e.getQualityFor("video"),
					});
				},
				we = {
					exportEvent: function (e) {
						return me(
							ue(e, "canPlay").pipe(
								fe(new ot.manager.PlayerEvent({ Type: "canplay" }))
							),
							ue(e, "playbackPlaying").pipe(
								j(function (e) {
									return new ot.manager.PlayerEvent({ Type: "playing" });
								})
							),
							ue(e, "playbackPaused").pipe(
								j(function () {
									return new ot.manager.PlayerEvent({ Type: "paused" });
								})
							),
							ue(e, "bufferStalled").pipe(
								j(function (e) {
									return new ot.manager.PlayerEvent({
										Type: "bufferstalled",
										MediaType: e.mediaType,
									});
								})
							),
							ue(e, "qualityChangeRequested").pipe(
								j(function (e) {
									return new ot.manager.PlayerEvent({
										Type: "qualitychangerequested",
										MediaType: e.mediaType,
										Quality: e.newQuality,
									});
								})
							),
							ue(e, "qualityChangeRendered").pipe(
								K(function (t) {
									var n = [
										new ot.manager.PlayerEvent({
											Type: "qualitychangerendered",
											MediaType: t.mediaType,
											Quality: t.newQuality,
										}),
									];
									return "video" === t.mediaType && n.push(be(e)), n;
								})
							),
							ce(5e4).pipe(fe(be(e))),
							ce(1e3).pipe(
								K(function () {
									return ["audio", "video"].map(function (t) {
										return new ot.manager.PlayerEvent({
											Type: "bufferlength",
											MediaType: t,
											BufferLength: e.getBufferLength(t),
										});
									});
								})
							)
						);
					},
					adaptPlayer: function (e, t) {
						e.extend(
							"XHRLoader",
							function (e) {
								var n = (e = e || {}).requestModifier;
								return {
									load: function (e) {
										var r = new Date(),
											i = e.request,
											o = new XMLHttpRequest();
										"MediaSegment" === i.type && (o = t.createEBXHR()),
											o.open(e.method, e.url, !0),
											i.responseType && (o.responseType = i.responseType),
											i.range &&
												o.setRequestHeader("Range", "bytes=" + i.range),
											i.requestStartDate || (i.requestStartDate = r),
											n && (o = n.modifyRequestHeader(o)),
											(o.withCredentials = e.withCredentials),
											(o.onload = e.onload),
											(o.onloadend = e.onend),
											(o.onerror = e.onerror),
											(o.onprogress = e.progress),
											(o.onabort = e.onabort),
											o.send(),
											(e.response = o);
									},
									abort: function (e) {
										var t = e.response;
										t.onloadend = t.onerror = t.onprogress = void 0;
									},
								};
							},
							!0
						);
					},
				},
				Se = (function () {
					function e(e) {
						e && e.xhrSetup && (this.xhrSetup = e.xhrSetup),
							(performance = performance),
							(XMLHttpRequest = XMLHttpRequest);
					}
					return (
						(e.prototype.destroy = function () {
							this.abort(), (this.loader = null);
						}),
						(e.prototype.abort = function () {
							var e = this.loader;
							e && 4 !== e.readyState && ((this.stats.aborted = !0), e.abort()),
								window.clearTimeout(this.requestTimeout),
								(this.requestTimeout = null),
								window.clearTimeout(this.retryTimeout),
								(this.retryTimeout = null);
						}),
						(e.prototype.load = function (e, t, n) {
							(this.context = e),
								(this.config = t),
								(this.callbacks = n),
								(this.stats = { trequest: performance.now(), retry: 0 }),
								(this.retryDelay = t.retryDelay),
								this.loadInternal();
						}),
						(e.prototype.loadInternal = function () {
							var e = this.context;
							this.loader = new XMLHttpRequest();
							var t = this.loader,
								n = this.stats;
							(n.tfirst = 0), (n.loaded = 0);
							var r = this.xhrSetup;
							try {
								if (r)
									try {
										r(t, e.url);
									} catch (n) {
										t.open("GET", e.url, !0), r(t, e.url);
									}
								t.readyState || t.open("GET", e.url, !0);
							} catch (n) {
								return void this.callbacks.onError(
									{ code: t.status, text: n.message },
									e,
									t
								);
							}
							e.rangeEnd &&
								t.setRequestHeader(
									"Range",
									"bytes=" + e.rangeStart + "-" + (e.rangeEnd - 1)
								),
								(t.onreadystatechange = this.readystatechange.bind(this)),
								(t.onprogress = this.loadprogress.bind(this)),
								(t.responseType = e.responseType),
								(this.requestTimeout = window.setTimeout(
									this.loadtimeout.bind(this),
									this.config.timeout
								)),
								t.send();
						}),
						(e.prototype.readystatechange = function (e) {
							var t = e.currentTarget,
								n = t.readyState,
								r = this.stats,
								i = this.context,
								o = this.config;
							if (!r.aborted)
								if (n < 2)
									this.requestTimeout = window.setTimeout(
										this.loadtimeout.bind(this),
										o.timeout
									);
								else if (
									(window.clearTimeout(this.requestTimeout),
									0 === r.tfirst &&
										(r.tfirst = Math.max(performance.now(), r.trequest)),
									4 === n)
								) {
									var s = t.status;
									if (s >= 200 && s < 300) {
										r.tload = Math.max(r.tfirst, performance.now());
										var a = void 0;
										"arraybuffer" === i.responseType
											? (a = t.response).byteLength
											: (a = t.responseText).length,
											(r.loaded = r.total = t.bytesReceived);
										var u = { url: t.responseURL, data: a };
										this.callbacks.onSuccess(u, r, i, t);
									} else
										r.retry >= o.maxRetry || (s >= 400 && s < 499)
											? (console.error(s + " while loading " + i.url),
											  this.callbacks.onError(
													{ code: s, text: t.statusText },
													i,
													t
											  ))
											: (console.warn(
													s +
														" while loading " +
														i.url +
														", retrying in " +
														this.retryDelay +
														"..."
											  ),
											  this.destroy(),
											  (this.retryTimeout = window.setTimeout(
													this.loadInternal.bind(this),
													this.retryDelay
											  )),
											  (this.retryDelay = Math.min(
													2 * this.retryDelay,
													o.maxRetryDelay
											  )),
											  r.retry++);
								}
						}),
						(e.prototype.loadtimeout = function () {
							console.warn("timeout while loading " + this.context.url),
								this.callbacks.onTimeout(this.stats, this.context, null);
						}),
						(e.prototype.loadprogress = function (e) {
							var t = e.currentTarget,
								n = this.stats;
							(n.loaded = e.loaded), e.lengthComputable && (n.total = e.total);
							var r = this.callbacks.onProgress;
							r && r(n, this.context, null, t);
						}),
						e
					);
				})(),
				Pe = (function () {
					var e = function (t, n) {
						return (e =
							Object.setPrototypeOf ||
							({ __proto__: [] } instanceof Array &&
								function (e, t) {
									e.__proto__ = t;
								}) ||
							function (e, t) {
								for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
							})(t, n);
					};
					return function (t, n) {
						function r() {
							this.constructor = t;
						}
						e(t, n),
							(t.prototype =
								null === n
									? Object.create(n)
									: ((r.prototype = n.prototype), new r()));
					};
				})(),
				ve = function (e, t) {
					return new ot.manager.PlayerEvent({
						Type: "register",
						Codec:
							(e.levels[t] && e.levels[t].attrs && e.levels[t].attrs.CODECS) ||
							"-",
						TimeShift: 0,
						Quality: t,
					});
				},
				Ae = function (e, t) {
					return (
						void 0 === t && (t = 0),
						e.streamController.mediaBuffer &&
						t < e.streamController.mediaBuffer.buffered.length
							? e.media.currentTime >=
									e.streamController.mediaBuffer.buffered.start(t) &&
							  e.media.currentTime <=
									e.streamController.mediaBuffer.buffered.end(t)
								? e.streamController.mediaBuffer.buffered.end(t) -
								  e.media.currentTime
								: Ae(e, t + 1)
							: NaN
					);
				};
			function Oe(e, t, n) {
				return (
					void 0 === n && (n = !0),
					(function (n) {
						function r() {
							return (null !== n && n.apply(this, arguments)) || this;
						}
						return (
							Pe(r, n),
							(r.prototype.load = function (e, n, r) {
								(this.context = e),
									(this.config = n),
									(this.callbacks = r),
									(this.stats = { trequest: performance.now(), retry: 0 }),
									(this.retryDelay = n.retryDelay),
									t.seekDrag || this._xhr(e.url, n, r, n);
							}),
							(r.prototype._xhr = function (t, n, r, i) {
								var o = this,
									s = this.stats,
									a = this.context,
									u = (function () {
										var e = function () {},
											t = {
												addEventListener: function () {},
												isAborted: !1,
												getAllResponseHeaders: function () {
													return "";
												},
												open: e,
												overrideMimeType: e,
												readyState: 1,
												send: e,
												setRequestHeader: e,
												abort: e,
											};
										return (
											(t.abort = function () {
												t.isAborted = !0;
											}),
											t
										);
									})();
								(u.responseType = a.responseType),
									(s.tfirst = 0),
									(s.loaded = 0),
									(u.requestTime = Date.now()),
									e
										.getResource(t)
										.then(function (e) {
											(u.responseTime = Date.now()),
												(u.response = e.buffer),
												(u.responseType = "arraybuffer"),
												(u.bytesReceived = e.byteLength || 0),
												(u.roundTripTime = u.responseTime - u.requestTime),
												(u.bandwidth = Math.floor(
													u.bytesReceived / u.roundTripTime
												)),
												(s.bw = 8 * u.bandwidth * 1e3),
												(u.responseType = "arraybuffer"),
												(u.readyState = 4),
												(u.status = 200),
												0 === s.tfirst &&
													(s.tfirst = Math.max(performance.now(), s.trequest)),
												(s.tload = Math.max(s.tfirst, performance.now())),
												(s.loaded = u.bytesReceived),
												(s.total = s.loaded);
											try {
												u.isAborted ||
													r.onSuccess(
														{ url: t, data: e.buffer },
														o.stats,
														a,
														u
													);
											} catch (e) {
												console.warn(e), console.warn(e.stack);
											}
										})
										.catch(function (e) {
											console.error(e),
												(u.readyState = 1),
												(u.timedout = !0),
												(o.context = a),
												(o.config = i),
												(o.callbacks = r),
												o.loadInternal(),
												r.onError({ code: u.status, text: e.message }, a, u);
										});
							}),
							r
						);
					})(Se)
				);
			}
			var Te = {
					exportEvent: function (e) {
						var t = !1,
							n = 0,
							r = 0,
							i = !1,
							o = e[0],
							s = e[1],
							a = new E();
						s.addEventListener("pause", function () {
							a.next(new ot.manager.PlayerEvent({ Type: "paused" }));
						}),
							s.addEventListener("playing", function () {
								a.next(new ot.manager.PlayerEvent({ Type: "playing" })),
									t || (a.next(ve(o, o.currentLevel)), (t = !0));
							}),
							s.addEventListener("canplay", function () {
								a.next(new ot.manager.PlayerEvent({ Type: "canplay" }));
							}),
							s.addEventListener("error", function () {
								a.next(new ot.manager.PlayerEvent({ Type: "error" }));
							});
						var u = ue(o, "bufferStalledError").pipe(
								fe(new ot.manager.PlayerEvent({ Type: "bufferstalled" }))
							),
							c = ue(o, "hlsLevelLoading").pipe(
								K(function (e) {
									return [
										new ot.manager.PlayerEvent({
											Type: "qualitychangerequested",
											MediaType: "video",
											Quality: e[1].level,
										}),
										ve(o, e[1].level),
									];
								})
							),
							l = ue(o, "hlsLevelLoaded").pipe(
								K(function (e) {
									return [
										new ot.manager.PlayerEvent({
											Type: "qualitychangerendered",
											MediaType: "video",
											Quality: e[1].level,
										}),
									];
								})
							),
							f = ce(5e4).pipe(
								j(function () {
									return ve(o, o.currentLevel);
								})
							),
							p = ce(1e3).pipe(
								K(function () {
									return ["video"].map(function (e) {
										return new ot.manager.PlayerEvent({
											Type: "bufferlength",
											MediaType: e,
											BufferLength: Ae(o),
										});
									});
								})
							);
						ce(1e3).subscribe(function () {
							r = o.media.currentTime;
							!i &&
								r < n + 0.03 &&
								!o.media.paused &&
								(a.next(new ot.manager.PlayerEvent({ Type: "bufferstalled" })),
								(i = !0)),
								i &&
									r > n + 0.03 &&
									!o.media.paused &&
									(a.next(new ot.manager.PlayerEvent({ Type: "playing" })),
									(i = !1)),
								(n = r);
						});
						return me(a, c, l, u, f, p);
					},
					adaptPlayer: function (e, t) {
						var n = e[0],
							r = e[1];
						(n.config.fLoader = Oe(t, n, !0)),
							r.addEventListener("timeupdate", function () {
								n.config.fLoader = Oe(t, n, !0);
							});
					},
				},
				Ce = (function () {
					var e = function (t, n) {
						return (e =
							Object.setPrototypeOf ||
							({ __proto__: [] } instanceof Array &&
								function (e, t) {
									e.__proto__ = t;
								}) ||
							function (e, t) {
								for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
							})(t, n);
					};
					return function (t, n) {
						function r() {
							this.constructor = t;
						}
						e(t, n),
							(t.prototype =
								null === n
									? Object.create(n)
									: ((r.prototype = n.prototype), new r()));
					};
				})(),
				Re = function (e, t) {
					return new ot.manager.PlayerEvent({
						Type: "register",
						Codec:
							(e.levels[t] && e.levels[t].attrs && e.levels[t].attrs.CODECS) ||
							"-",
						TimeShift: 0,
						Quality: t,
					});
				},
				Ee = function (e, t) {
					return (
						void 0 === t && (t = 0),
						e.streamController.mediaBuffer &&
						t < e.streamController.mediaBuffer.buffered.length
							? e.media.currentTime >=
									e.streamController.mediaBuffer.buffered.start(t) &&
							  e.media.currentTime <=
									e.streamController.mediaBuffer.buffered.end(t)
								? e.streamController.mediaBuffer.buffered.end(t) -
								  e.media.currentTime
								: Ee(e, t + 1)
							: NaN
					);
				};
			var Me = 0,
				Le = {
					exportEvent: function (e) {
						var t = !1,
							n = 0,
							r = 0,
							i = !1,
							o = e[0],
							s = e[1],
							a = new E();
						s.addEventListener("pause", function () {
							a.next(new ot.manager.PlayerEvent({ Type: "paused" }));
						}),
							s.addEventListener("playing", function () {
								a.next(new ot.manager.PlayerEvent({ Type: "playing" })),
									t || (a.next(Re(o, o.currentLevel)), (t = !0));
							}),
							s.addEventListener("seeking", function (e) {
								Math.abs(e.target.currentTime - Me) > 2 &&
									a.next(
										new ot.manager.PlayerEvent({
											Type: "seeking",
											CurrentTime: e.target.currentTime,
										})
									);
							}),
							s.addEventListener("canplay", function () {
								a.next(new ot.manager.PlayerEvent({ Type: "canplay" }));
							}),
							s.addEventListener("error", function () {
								a.next(new ot.manager.PlayerEvent({ Type: "error" }));
							});
						var u = ue(o, "bufferStalledError").pipe(
								fe(new ot.manager.PlayerEvent({ Type: "bufferstalled" }))
							),
							c = ue(o, "hlsLevelLoading").pipe(
								K(function (e) {
									return [
										new ot.manager.PlayerEvent({
											Type: "qualitychangerequested",
											MediaType: "video",
											Quality: e[1].level,
										}),
										Re(o, e[1].level),
									];
								})
							),
							l = ue(o, "hlsLevelLoaded").pipe(
								K(function (e) {
									return [
										new ot.manager.PlayerEvent({
											Type: "qualitychangerendered",
											MediaType: "video",
											Quality: e[1].level,
										}),
									];
								})
							),
							f = ce(5e4).pipe(
								j(function () {
									return Re(o, o.currentLevel);
								})
							),
							p = ce(1e4).pipe(
								j(function () {
									return (function (e) {
										return new ot.manager.PlayerEvent({
											Type: "currentTime",
											CurrentTime: e.media.currentTime,
										});
									})(o);
								})
							),
							h = ce(1e3).pipe(
								K(function () {
									return (
										(Me = s.currentTime),
										["video"].map(function (e) {
											return new ot.manager.PlayerEvent({
												Type: "bufferlength",
												MediaType: e,
												BufferLength: Ee(o),
											});
										})
									);
								})
							);
						ce(1e3).subscribe(function () {
							if (o.media) {
								r = o.media.currentTime;
								!i &&
									r < n + 0.03 &&
									!o.media.paused &&
									(a.next(
										new ot.manager.PlayerEvent({ Type: "bufferstalled" })
									),
									(i = !0)),
									i &&
										r > n + 0.03 &&
										!o.media.paused &&
										(a.next(new ot.manager.PlayerEvent({ Type: "playing" })),
										(i = !1)),
									(n = r);
							}
						});
						return me(a, c, l, u, f, h, p);
					},
					adaptPlayer: function (e, t) {
						var n = e[0];
						e[1];
						n.config.fLoader = (function (e, t, n, r) {
							return (
								void 0 === n && (n = !0),
								(function (t) {
									function n() {
										return (null !== t && t.apply(this, arguments)) || this;
									}
									return (
										Ce(n, t),
										(n.prototype.loadInternal = function () {
											var t = this.config,
												n = this.context;
											if (t) {
												var r = (this.loader = e.createEBXHR()),
													i = this.stats;
												(i.loading.first = 0), (i.loaded = 0);
												var o = this.xhrSetup;
												try {
													if (o)
														try {
															o(r, n.url);
														} catch (e) {
															r.open("GET", n.url, !0), o(r, n.url);
														}
													r.readyState || r.open("GET", n.url, !0);
												} catch (e) {
													return void this.callbacks.onError(
														{ code: r.status, text: e.message },
														n,
														r
													);
												}
												n.rangeEnd &&
													r.setRequestHeader(
														"Range",
														"bytes=" + n.rangeStart + "-" + (n.rangeEnd - 1)
													),
													(r.onreadystatechange =
														this.readystatechange.bind(this)),
													(r.onprogress = this.loadprogress.bind(this)),
													(r.responseType = n.responseType),
													self.clearTimeout(this.requestTimeout),
													(this.requestTimeout = self.setTimeout(
														this.loadtimeout.bind(this),
														t.timeout
													)),
													r.send();
											}
										}),
										n
									);
								})(r)
							);
						})(t, 0, !0, n.config.loader);
					},
				},
				xe = function (e) {
					return new ot.manager.PlayerEvent({
						Type: "register",
						Codec: e.codec || "-",
						TimeShift: 0,
						Quality: e.quality || 0,
					});
				},
				De = {
					exportEvent: function (e) {
						var t = !1,
							n = new E();
						e.addListener &&
							(e.addListener("pause", function () {
								n.next(new ot.manager.PlayerEvent({ Type: "paused" }));
							}),
							e.addListener("playing", function () {
								n.next(new ot.manager.PlayerEvent({ Type: "playing" })),
									t || (n.next(xe(e)), (t = !0));
							}),
							e.addListener("canplay", function () {
								n.next(new ot.manager.PlayerEvent({ Type: "canplay" }));
							}),
							e.addListener("error", function () {
								n.next(new ot.manager.PlayerEvent({ Type: "error" }));
							}),
							e.addListener("qualitychangerequested", function () {
								n.next(
									new ot.manager.PlayerEvent({
										Type: "qualitychangerequested",
										MediaType: "video",
										Quality: e.quality,
									})
								);
							}),
							e.addListener("qualitychangerendered", function () {
								n.next(
									new ot.manager.PlayerEvent({
										Type: "qualitychangerendered",
										MediaType: "video",
										Quality: e.quality,
									})
								),
									n.next(xe(e));
							}));
						var r = ce(5e4).pipe(
								j(function () {
									return xe(e);
								})
							),
							i = ce(1e3).pipe(
								j(function () {
									return new ot.manager.PlayerEvent({
										Type: "bufferlength",
										MediaType: "video",
										BufferLength: e.bufferLength || 0,
									});
								})
							);
						return me(n, r, i);
					},
					adaptPlayer: function (e, t) {},
				},
				Ie = function () {
					return (Ie =
						Object.assign ||
						function (e) {
							for (var t, n = 1, r = arguments.length; n < r; n++)
								for (var i in (t = arguments[n]))
									Object.prototype.hasOwnProperty.call(t, i) && (e[i] = t[i]);
							return e;
						}).apply(this, arguments);
				},
				ke = function (e) {
					return new ot.manager.PlayerEvent({
						Type: "register",
						Codec: "-",
						TimeShift: 0,
						Quality: 0,
					});
				},
				je = {
					exportEvent: function (e) {
						return me(
							ue(e, "canPlay").pipe(
								fe(new ot.manager.PlayerEvent({ Type: "canplay" }))
							),
							ue(e, "playbackPlaying").pipe(
								j(function (e) {
									return new ot.manager.PlayerEvent({ Type: "playing" });
								})
							),
							ue(e, "playbackPaused").pipe(
								j(function () {
									return new ot.manager.PlayerEvent({ Type: "paused" });
								})
							),
							ue(e, "bufferStalled").pipe(
								j(function (e) {
									return new ot.manager.PlayerEvent({
										Type: "bufferstalled",
										MediaType: e.mediaType,
									});
								})
							),
							ue(e, "qualityChangeRequested").pipe(
								j(function (e) {
									return new ot.manager.PlayerEvent({
										Type: "qualitychangerequested",
										MediaType: e.mediaType,
										Quality: e.newQuality,
									});
								})
							),
							ue(e, "qualityChangeRendered").pipe(
								K(function (e) {
									var t = [
										new ot.manager.PlayerEvent({
											Type: "qualitychangerendered",
											MediaType: e.mediaType,
											Quality: e.newQuality,
										}),
									];
									return "video" === e.mediaType && t.push(ke()), t;
								})
							),
							ce(5e4).pipe(fe(ke())),
							ce(1e3).pipe(
								K(function () {
									return ["audio", "video"].map(function (e) {
										return new ot.manager.PlayerEvent({
											Type: "bufferlength",
											MediaType: e,
											BufferLength: 0,
										});
									});
								})
							)
						);
					},
					adaptPlayer: function (e, t) {
						var n = (e = e[0]).xhr;
						e.xhr = function (e, r) {
							if (-1 === e.uri.indexOf(".ts")) return n(e, r);
							var i = new (function () {
								var e = this;
								(this.open = function (t, n) {
									(e.state = "opened"), (e.url = n);
								}),
									(this.addEventListener = function () {}),
									(this.send = function () {
										t.getResource(e.url).then(function (t) {
											(e.response = t.buffer),
												(e.status = 200),
												(e.readyState = 4),
												e.onreadystatechange && e.onreadystatechange(),
												e.onload && e.onload();
										});
									}),
									(this.abort = function () {});
							})();
							return n(Ie(Ie({}, e), { xhr: i }), r);
						};
					},
				},
				Be = new Map(),
				Ne = function (e, t) {
					Be.has(e) &&
						console.warn("replacing the adapter for " + e + " player"),
						Be.set(e, t);
				};
			Ne("dash", we),
				Ne("hls", Le),
				Ne("hls014", Te),
				Ne("rn", De),
				Ne("videojs", je);
			var Ue = parseFloat(window.epsilon_min) || 0.1,
				_e = [
					[0, 1e3],
					[1e3, 2e3],
					[2e3, 3e3],
					[3e3, 4e3],
				],
				qe = window.reward_func || "enup_dislong",
				Ve = parseFloat(window.alpha || "0.7"),
				Fe = parseFloat(window.gamma || "0.5"),
				ze = window.algo || "qlwait";
			console.info("EPSILON MIN!!! ", Ue),
				console.info("USING REWARD FUNCTION!!!", qe),
				console.info("ALPHA !!!!!", Ve),
				console.info("GAMMA !!!!!", Fe);
			window.expId, window.hostname;
			var We = (function () {
					var e = function (t, n) {
						return (e =
							Object.setPrototypeOf ||
							({ __proto__: [] } instanceof Array &&
								function (e, t) {
									e.__proto__ = t;
								}) ||
							function (e, t) {
								for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
							})(t, n);
					};
					return function (t, n) {
						function r() {
							this.constructor = t;
						}
						e(t, n),
							(t.prototype =
								null === n
									? Object.create(n)
									: ((r.prototype = n.prototype), new r()));
					};
				})(),
				He = function (e, t) {
					var n = "function" == typeof Symbol && e[Symbol.iterator];
					if (!n) return e;
					var r,
						i,
						o = n.call(e),
						s = [];
					try {
						for (; (void 0 === t || t-- > 0) && !(r = o.next()).done; )
							s.push(r.value);
					} catch (e) {
						i = { error: e };
					} finally {
						try {
							r && !r.done && (n = o.return) && n.call(o);
						} finally {
							if (i) throw i.error;
						}
					}
					return s;
				},
				Ge = function () {
					for (var e = [], t = 0; t < arguments.length; t++)
						e = e.concat(He(arguments[t]));
					return e;
				},
				Qe = function (e, t, n, r) {
					return t + 1e-5 > r[e] ? n : e;
				},
				Je = (function () {
					function e() {
						(this.cumReward = 0),
							(this.epsilon = 0.2),
							(this.policy = this.loadParameter());
					}
					return (
						(e.prototype.quantizeState = function (e) {
							var t = null == e ? void 0 : e.bufferLength;
							if (!1 === Number.isFinite(t)) return 0;
							var n = Math.floor(Math.max(0, t) / 4);
							return (n = n > 7 ? 7 : n);
						}),
						(e.prototype.act = function (e, t, n) {
							this.lastState &&
								this.lastAction &&
								((this.cumReward += t.value),
								this.updateLocalParamter(
									this.lastState,
									e,
									this.lastAction,
									t
								));
							var r = this.quantizeState(e),
								i = this.policy[r].reduce(Qe, 0),
								o = Math.random() <= this.epsilon;
							return (
								o && (i = Math.floor(2 * Math.random())),
								(this.lastState = e),
								(this.lastAction = { useV2V: 1 === i }),
								console.info(
									"RL: Take " + (o ? "[rand]" : "[best]") + " action: ",
									i,
									e
								),
								this.lastAction
							);
						}),
						(e.prototype.updateLocalParamter = function (e, t, n, r) {
							var i = this.quantizeState(e),
								o = this.quantizeState(t);
							if (
								(console.info("RL: Update local parameter", e, t, n, r),
								Array.isArray(this.policy[o]))
							) {
								var s = this.policy[i][n.useV2V ? 1 : 0];
								(this.policy[i][n.useV2V ? 1 : 0] =
									s +
									0.4 *
										(r.value +
											0.25 * Math.max.apply(Math, Ge(this.policy[o])) -
											s)),
									this.saveParameter(),
									this.loadParameter(),
									console.info(JSON.stringify(this.policy));
							}
						}),
						(e.prototype.policyJson = function () {
							return JSON.stringify(this.policy);
						}),
						(e.prototype.saveParameter = function () {
							localStorage.setItem("rlparam.v1", this.policyJson());
						}),
						(e.prototype.loadParameter = function () {
							var e = localStorage.getItem("rlparam.v1");
							return e
								? JSON.parse(e)
								: Array.from(Array(8)).map(function (e) {
										return [0, 1];
								  });
						}),
						(e.prototype.getCumReward = function () {
							return this.cumReward;
						}),
						(e.prototype.feedback = function (e, t, n, r, i) {}),
						e
					);
				})(),
				Ye = (function () {
					function e(e) {
						void 0 === e && (e = { gamma: 0.9, alpha: 0.9 }),
							(this.nState = 16),
							(this.cumReward = 0),
							(this.nAction = 4),
							(this.localStorageID = "rlparam.v7"),
							(this.epsilon = 0.9),
							(this.epsilonMin = Ue),
							(this.alpha = 0.4),
							(this.gamma = 0.9),
							(this.actions = _e),
							(this.step = 0),
							(this.policy = this.loadOrCreate()),
							(this.nAction = this.actions.length),
							(this.gamma = e.gamma),
							(this.alpha = e.alpha);
					}
					return (
						(e.prototype.setEpsilon = function (e) {
							this.epsilon = Math.min(1, Math.max(e, this.epsilonMin));
						}),
						(e.prototype.act = function (e, t) {
							void 0 === t && (t = !1);
							var n = this.policy[e].reduce(Qe, 0);
							return (
								(Math.random() <= this.epsilon || t) &&
									(n = Math.floor((Math.random() / 1.01) * this.nAction)),
								n
							);
						}),
						(e.prototype.restartPolicy = function () {
							var e = this;
							this.policy = Array.from(Array(this.nState)).map(function (t) {
								return Array(e.actions.length)
									.fill(0)
									.map(function (e) {
										return Math.random();
									});
							});
						}),
						(e.prototype.loadOrCreate = function () {
							var e = this;
							return Array.from(Array(this.nState)).map(function (t) {
								return Array(e.actions.length)
									.fill(0)
									.map(function (e) {
										return Math.random();
									});
							});
						}),
						(e.prototype.feedback = function (e, t, n, r, i) {
							console.assert(e < this.nState),
								console.assert(r < this.nState),
								console.assert(t < this.nAction);
							var o = this.policy[e][t];
							(this.policy[e][t] =
								o +
								this.alpha *
									(n +
										this.gamma * Math.max.apply(Math, Ge(this.policy[r])) -
										o)),
								(this.policy = JSON.parse(JSON.stringify(this.policy)));
						}),
						(e.prototype.infoToState = function (e, t, n, r) {
							var i = 0;
							return (
								n > 0 && (i += 1),
								r > 0 && (i += 2),
								(e < 10 ? 1 : 0) + 2 * (t < 3 ? 1 : 0) + 4 * i
							);
						}),
						(e.prototype.translateAction = function (e) {
							if (e >= this.actions.length)
								throw Error(
									"Action " + e + " doest not exist on " + this.actions
								);
							return this.actions[e];
						}),
						(e.prototype.policyJson = function () {
							return JSON.stringify(this.policy);
						}),
						e
					);
				})(),
				Ke =
					((function (e) {
						function t() {
							return (null !== e && e.apply(this, arguments)) || this;
						}
						We(t, e);
					})(Ye),
					(function (e) {
						function t() {
							var t = (null !== e && e.apply(this, arguments)) || this;
							return (t.nState = 1), (t.localStorageID = "rlparam.orb"), t;
						}
						return (
							We(t, e),
							(t.prototype.infoToState = function (e, t, n, r) {
								return 0;
							}),
							t
						);
					})(Ye)),
				Xe = (function (e) {
					function t() {
						var t = (null !== e && e.apply(this, arguments)) || this;
						return (t.nState = 4), t;
					}
					return (
						We(t, e),
						(t.prototype.infoToState = function (e, t, n, r) {
							return (e < 10 ? 1 : 0) + 2 * (t < 3 ? 1 : 0);
						}),
						t
					);
				})(Ye);
			var $e = function (e, t) {
					var n = "function" == typeof Symbol && e[Symbol.iterator];
					if (!n) return e;
					var r,
						i,
						o = n.call(e),
						s = [];
					try {
						for (; (void 0 === t || t-- > 0) && !(r = o.next()).done; )
							s.push(r.value);
					} catch (e) {
						i = { error: e };
					} finally {
						try {
							r && !r.done && (n = o.return) && n.call(o);
						} finally {
							if (i) throw i.error;
						}
					}
					return s;
				},
				Ze = function () {
					for (var e = [], t = 0; t < arguments.length; t++)
						e = e.concat($e(arguments[t]));
					return e;
				};
			console.info("Using algorithm !!!!! ", ze);
			var et = function (e, t, n) {
				(this.sizeBytes = e),
					(this.timespent = t),
					(this.at = new Date()),
					(this.type = n);
			};
			function tt(e, t) {
				var n,
					r = [],
					i = 0,
					o = 0;
				return (
					e.forEach(function (e, n) {
						e.at >= new Date(+new Date().getTime() - 3e4) &&
							(r.push(e),
							e.type == t && ((i += e.sizeBytes), (o += e.timespent)));
					}),
					0 !== i && 0 != o && (n = i / o),
					{ throughput: n, newList: r }
				);
			}
			var nt,
				rt = (function () {
					function e(e) {
						var t = this;
						(this.qlC = new Je()),
							(this.qlCWaiting = (function (e) {
								if ("orb" === e) return new Ke({ alpha: Ve, gamma: Fe });
								if ("qlnpr" == e) return new Xe({ alpha: Ve, gamma: Fe });
								if ("qlwait" == e) return new Ye({ alpha: Ve, gamma: Fe });
								throw Error("No such algorithm");
							})(ze)),
							(this.experienceStore = []),
							(this.episodeDone = !1),
							(this.lastRebufferCntRL = 0),
							(this.lastV2VCntRL = 0),
							(this.lastSucV2VSentRL = 0),
							(this.lastCDNCntRL = 0),
							(this.revertCDNRL = 0),
							(this.lastV2VSendCntRL = 0),
							(this.qlWaitingStep = 0),
							(this.qlWaitingReward = 0),
							(this.lastRebufferCnt = 0),
							(this.currentQualityLevel = 0),
							(this.switchUp = 0),
							(this.switchDown = 0),
							(this.last30SecondsDownload = []),
							(this.bufferedDownloads = []),
							(this.bufferedUploads = []),
							(this.snapShotNeighbours = void 0),
							(this.bufferLengthRecords = []),
							(this.lastBufferLength = 0),
							(this.chunkSizeMapping = new Map()),
							(this.throughputMapping = new Map()),
							(this.nChunks = 10),
							(this.defaultDownloadTimeMs = 1e3),
							(this.swarmManager = e),
							setInterval(function () {
								return t.reportStats();
							}, 1e4),
							this.throughputMapping.set("cdn", []),
							this.throughputMapping.set("v2v", []),
							setTimeout(function () {
								t.episodeDone = !0;
							}, 3e5),
							setTimeout(function () {
								t.qlCWaiting.restartPolicy();
							}, 24e5);
					}
					return (
						(e.prototype.reportStats = function () {}),
						(e.prototype.reportP2PGraph = function (e, t, n, r) {}),
						(e.prototype.reportEpisodeReward = function (e, t, n, r, i) {
							void 0 === i && (i = "[]");
						}),
						(e.prototype.addSuccessUpload = function () {
							this.lastSucV2VSentRL++;
						}),
						(e.prototype.addRevertCDN = function (e) {}),
						(e.prototype.addUpload = function (e) {
							this.bufferedUploads.push(e), this.lastV2VSendCntRL++;
						}),
						(e.prototype.addDownload = function (e, t, n) {
							"v2v" == n ? this.lastV2VCntRL++ : this.lastCDNCntRL++;
							var r = new et(e, t, n);
							this.last30SecondsDownload.push(r),
								this.bufferedDownloads.push(r),
								this.chunkSizeMapping.has(this.currentQualityLevel) ||
									this.chunkSizeMapping.set(this.currentQualityLevel, [0, 0]);
							var i = this.chunkSizeMapping.get(this.currentQualityLevel),
								o = [(i[0] * i[1] + e) / (i[1] + 1), i[1] + 1],
								s = e / t;
							this.chunkSizeMapping.set(this.currentQualityLevel, o);
							var a = this.throughputMapping.get(n);
							a.push(s), a.length > this.nChunks && a.shift();
						}),
						(e.prototype.estimateV2VTime = function () {
							var e = this.chunkSizeMapping.get(this.currentQualityLevel),
								t = this.throughputMapping.get("v2v");
							if (!e || 0 == t.length) return this.defaultDownloadTimeMs;
							var n =
								t.reduce(function (e, t) {
									return e + t;
								}) / t.length;
							return e[0] / n;
						}),
						(e.prototype.safeToUseV2V = function (e, t) {
							if ((void 0 === e && (e = !1), void 0 === t && (t = 0), e))
								return this.getActionV2V().useV2V;
							if (0 != t) return this.lastBufferLength > t;
							var n = this.estimateV2VTime();
							return 1e3 * this.lastBufferLength > n;
						}),
						(e.prototype.getP2PThroughput = function () {
							var e = tt(this.last30SecondsDownload, "v2v");
							return (
								(this.last30SecondsDownload = e.newList),
								e.throughput && (this.lastV2VThroughput = e.throughput),
								this.lastV2VThroughput
							);
						}),
						(e.prototype.getCDNThroughput = function () {
							var e = tt(this.last30SecondsDownload, "cdn");
							return (
								(this.last30SecondsDownload = e.newList),
								e.throughput && (this.lastCdnThroughput = e.throughput),
								this.lastCdnThroughput
							);
						}),
						(e.prototype.getSwarmSize = function () {
							return this.swarmManager.getSwarmSize();
						}),
						(e.prototype.addBufferLength = function (e) {
							null != e &&
								(this.bufferLengthRecords.push(e), (this.lastBufferLength = e));
						}),
						(e.prototype.addRebuffering = function () {
							var e = this;
							setTimeout(function () {
								return e.getActionV2V();
							}, 1e4),
								(this.lastRebufferCnt += 1),
								(this.lastRebufferCntRL += 1);
						}),
						(e.prototype.setQuality = function (e) {
							e > this.currentQualityLevel && (this.switchUp += 1),
								e < this.currentQualityLevel && (this.switchDown += 1),
								(this.currentQualityLevel = e);
						}),
						(e.prototype.getActionV2V = function () {
							var e = this.calculateReward();
							(this.lastCDNCntRL = 0),
								(this.lastV2VCntRL = 0),
								(this.lastV2VSendCntRL = 0),
								(this.lastRebufferCntRL = 0),
								(this.lastSucV2VSentRL = 0);
							var t = this.qlC.act(
								{ bufferLength: this.lastBufferLength },
								{ value: e.reward },
								e.done
							);
							return e.done || this.episodeDone, t;
						}),
						(e.prototype.getActionWaitingTime = function (e) {
							void 0 === e && (e = !1);
							var t = this.qlCWaiting.infoToState(
									this.lastBufferLength,
									this.swarmManager.getPeerList().size,
									this.lastCDNCntRL,
									this.lastV2VSendCntRL
								),
								n = this.qlCWaiting.act(t, e),
								r = this.calculateRewardWaitingTime(qe);
							if (
								(r &&
									void 0 !== this.lastAction &&
									void 0 !== this.lastState &&
									(this.experienceStore.push({
										s: this.lastState,
										a: this.lastAction,
										r: r.reward,
										ns: t,
										b: this.lastBufferLength,
										n: this.swarmManager.getPeerList().size,
									}),
									this.qlCWaiting.feedback(
										this.lastState,
										this.lastAction,
										r.reward || 0,
										t,
										r.done
									),
									(this.qlWaitingReward += r.reward)),
								(this.lastState = t),
								(this.lastAction = n),
								(this.lastCDNCntRL = 0),
								(this.lastV2VCntRL = 0),
								(this.lastV2VSendCntRL = 0),
								(this.lastRebufferCntRL = 0),
								(this.qlWaitingStep += 1),
								this.qlCWaiting.setEpsilon(0.975 * this.qlCWaiting.epsilon),
								this.qlWaitingStep % 20 == 19)
							) {
								var i = this.qlCWaiting.epsilon;
								if (this.snapShotNeighbours) {
									var o = Ze(this.swarmManager.getPeerList().keys()),
										s = (function (e, t) {
											if (0 == e.length) return 1;
											var n = e.filter(function (e) {
												return t.includes(e);
											}).length;
											return Math.min((e.length - n) / e.length, 1);
										})(this.snapShotNeighbours, o);
									1 == s && this.qlCWaiting.restartPolicy(),
										(this.snapShotNeighbours = o),
										(this.qlCWaiting.epsilon =
											this.qlCWaiting.epsilon +
											(0.9 - this.qlCWaiting.epsilon) * s);
								} else
									this.snapShotNeighbours = Ze(
										this.swarmManager.getPeerList().keys()
									);
								this.reportEpisodeReward(
									this.qlCWaiting.policyJson(),
									this.qlWaitingReward,
									i,
									this.qlCWaiting.epsilon,
									JSON.stringify(this.experienceStore)
								),
									(this.qlWaitingReward = 0);
							}
							return this.qlCWaiting.translateAction(n);
						}),
						(e.prototype.calculateReward = function () {
							return this.calculateRewardV2();
						}),
						(e.prototype.calculateRewardV1 = function () {
							return this.lastRebufferCntRL > 0
								? { reward: -1, done: !0 }
								: { reward: 0, done: !1 };
						}),
						(e.prototype.calculateRewardV2 = function () {
							return this.lastRebufferCntRL > 0
								? { reward: -1, done: !0 }
								: {
										reward:
											(this.lastV2VCntRL + this.lastV2VSendCntRL) /
											(this.lastCDNCntRL +
												this.lastV2VSendCntRL +
												this.lastV2VCntRL),
										done: !1,
								  };
						}),
						(e.prototype.calculateRewardWaitingTime = function (e) {
							if (this.lastRebufferCntRL > 0 || this.lastBufferLength < 6)
								return { reward: -this.lastRebufferCntRL - 1, done: !1 };
							if ("simple" == e)
								return { reward: this.lastV2VCntRL > 0 ? 1 : 0, done: !1 };
							if ("upload" == e)
								return { reward: this.lastV2VSendCntRL, done: !1 };
							if ("enhance_upload" == e)
								return {
									reward: Math.sqrt(this.lastV2VCntRL + this.lastV2VSendCntRL),
									done: !1,
								};
							if ("enup_dislong" == e) {
								var t = 1;
								return (
									void 0 !== this.lastAction &&
										(t *= Math.pow(0.9, this.lastAction)),
									{
										reward: Math.sqrt(
											this.lastV2VCntRL * t + this.lastV2VSendCntRL
										),
										done: !1,
									}
								);
							}
							return {
								reward:
									(this.lastV2VCntRL + this.lastV2VSendCntRL) /
									(this.lastCDNCntRL +
										this.lastV2VSendCntRL +
										this.lastV2VCntRL +
										1e-4),
								done: !1,
							};
						}),
						e
					);
				})(),
				it = n(3),
				ot = n(0);
			!(function (e) {
				(e[(e.PLAYING = 1)] = "PLAYING"),
					(e[(e.IDLE = 2)] = "IDLE"),
					(e[(e.BUFFERING = 3)] = "BUFFERING"),
					(e[(e.PAUSED = 4)] = "PAUSED"),
					(e[(e.STOP = 5)] = "STOP");
			})(nt || (nt = {}));
			var st,
				at = function () {
					var e = this;
					(this.origin = window.origin || ""),
						(this.bufferLength = -1),
						(this.state = ot.manager.PlayingState.PLAYING),
						(this.lastPlayingState = ot.manager.PlayingState.PLAYING),
						(this.rebuffers = 0),
						(this.reBufferingTime = 0),
						(this.lastRebufferingTime = 0),
						(this.playingTime = 0),
						(this.isAudio = !1),
						(this.isOnDemand = !1),
						(this.bandwidthFluctuation = 0),
						(this.timeshift = 0),
						(this.lastTimeshift = 0),
						(this.subscribeEvents = function () {
							return e.eventInfo;
						}),
						(this.start = function () {
							return (
								e.sendTimer && window.clearInterval(e.sendTimer),
								(e.sendTimer = window.setInterval(function () {
									e.sendPlayerInfo(),
										e.sendPlayerState(),
										e.sendPeerInfo(),
										e.sendPeerState(),
										(e.rebuffers = 0),
										(e.reBufferingTime = 0);
								}, 1e3)),
								e
							);
						}),
						(this.stop = function () {
							clearInterval(e.sendTimer),
								clearInterval(e.playingTimeTimer),
								clearInterval(e.rebufferTimeIntervalId);
						}),
						(this.getInitTime = function () {
							return Date.now();
						}),
						(this.reset = function () {}),
						(this.setOrigin = function (t) {
							e.origin = t;
						}),
						(this.setMobileOS = function (t) {
							e.osMobileString = t;
						}),
						(this.setMobileBrowser = function (t) {
							e.browserMobileString = t;
						}),
						(this.setContent = function (t) {
							e.content = t;
						}),
						(this.setProtocol = function (t) {
							e.protocol = t;
						}),
						(this.setBufferLength = function (t) {
							e.bufferLength = t;
						}),
						(this.setTimeshift = function (t) {
							(e.lastTimeshift = e.timeshift),
								(e.timeshift = t),
								t !== e.lastTimeshift && e.sendPlayerState();
						}),
						(this.setState = function (t) {
							e.state === ot.manager.PlayingState.BUFFERING &&
								t === ot.manager.PlayingState.PLAYING &&
								((e.lastRebufferingTime = void 0), (e.reBufferingTime = 0)),
								t === ot.manager.PlayingState.PAUSED
									? ot.manager.ArgumentsEvent.Actions.PAUSE
									: t === ot.manager.PlayingState.PLAYING
									? ot.manager.ArgumentsEvent.Actions.PLAY
									: t === ot.manager.PlayingState.STOP
									? ot.manager.ArgumentsEvent.Actions.STOP
									: ot.manager.ArgumentsEvent.Actions.REBUFFER,
								t === ot.manager.PlayingState.BUFFERING &&
								void 0 === e.lastRebufferingTime
									? (e.lastRebufferingTime = Date.now())
									: t === ot.manager.PlayingState.BUFFERING &&
									  "number" == typeof e.lastRebufferingTime &&
									  (e.reBufferingTime += 1),
								t === ot.manager.PlayingState.BUFFERING ||
								t === ot.manager.PlayingState.PLAYING
									? (void 0 !== e.playingTimeTimer &&
											window.clearInterval(e.playingTimeTimer),
									  (e.playingTimeTimer = window.setInterval(function () {
											e.playingTime = e.playingTime + 1;
									  }, 1e3)))
									: void 0 !== e.playingTimeTimer &&
									  window.clearInterval(e.playingTimeTimer),
								(e.state = t),
								t !== e.state && ((e.state = t), e.sendPlayerState()),
								e.rebufferTimeIntervalId &&
									window.clearInterval(e.rebufferTimeIntervalId),
								(e.rebufferTimeIntervalId = window.setInterval(function () {
									(3 !== e.state && 4 !== e.state) || (e.reBufferingTime += 1),
										e.state;
								}, 1e3));
						}),
						(this.setStartTime = function (t) {
							e.startTime = t;
						}),
						(this.incRebuffer = function () {
							e.rebuffers = e.rebuffers + 1;
						}),
						(this.setBandwidthFluctuation = function () {
							e.bandwidthFluctuation++;
						}),
						(this.setBandwidth = function (t) {
							(e.lastBandwidth = e.bandwidth),
								t !== e.lastBandwidth && e.sendPlayerState(),
								(e.bandwidth = t);
						}),
						(this.getOS = function () {
							switch (it.os.family) {
								case "Windows":
								case "Windows XP":
									e.os = e.getOSWindows();
									break;
								case "OS X":
									e.os = e.getOSOSX();
									break;
								case "Linux":
								case "Ubuntu":
								case "Debian":
								case "Fedora":
								case "Red Hat":
								case "SuSE":
									e.os = e.getOSLinux();
									break;
								case "Android":
									e.os = e.getOSAndroid();
									break;
								case "iOS":
									e.os = e.getOSiOS();
									break;
								case "Windows Phone":
									e.os = e.getOSWp();
									break;
								default:
									if (/windows/i.test(it.os.family)) {
										e.os = e.getOSWindows();
										break;
									}
									e.os = "NA";
							}
							return e.os;
						}),
						(this.getOSWindows = function () {
							switch (it.os.version) {
								case "10.0":
								case "10":
									return "w_10";
							}
							switch (it.os.family) {
								case "Windows NT 10.0":
								case "Windows NT 10":
								case "Windows NT 6.3":
									return "w_10";
								case "Windows NT 6.2":
									return "w_8";
								case "Windows NT 6.1":
									return "w_7";
								case "Windows XP":
									return "w_xp";
								default:
									return "w_old";
							}
						}),
						(this.getOSOSX = function () {
							return "string" == typeof it.os.version && it.os.version.length
								? "m_" + it.os.version
								: "m_old";
						}),
						(this.getOSLinux = function () {
							var e = it.os.family;
							return "Linux" === e
								? "l_other"
								: "l_" + (e = e.substr(0, 49).toLowerCase());
						}),
						(this.getOSAndroid = function () {
							return "string" == typeof it.os.version && it.os.version.length
								? "and_" + it.os.version
								: "and_old";
						}),
						(this.getOSiOS = function () {
							return "string" == typeof it.os.version && it.os.version.length
								? "ios_" + it.os.version
								: "ios_old";
						}),
						(this.getOSWp = function () {
							return "string" == typeof it.os.version && it.os.version.length
								? "wp_" + it.os.version
								: "wp_old";
						}),
						(this.getBrowser = function () {
							var t;
							switch (it.name) {
								case "Chrome":
									t = "chr";
									break;
								case "Firefox":
								case "Firefox for iOS":
									t = "ff";
									break;
								case "IE":
									t = "ie";
									break;
								case "Microsoft Edge":
									t = "e";
									break;
								case "Safari":
									t = "s";
									break;
								case "Opera Mini":
								case "Opera":
									t = "o";
									break;
								default:
									return void (e.browser = "na");
							}
							var n = /^(\d+).*/.exec(it.version);
							return (
								null === n && (e.browser = t + "_na"),
								(e.browser = t + "_" + n[1]),
								e.browser
							);
						}),
						(this.sendPeerInfo = function () {
							e.eventInfo.next(
								new ot.manager.Message({
									Type: ot.manager.MessageType.MessageTypeEvent,
									ArgumentsEvent: {
										EventName: ot.manager.ArgumentsEvent.EventClass.PEER,
										Action: ot.manager.ArgumentsEvent.Actions.INFO,
										ArgumentsPeerInfo: {
											Radio: e.isAudio,
											VOD: e.isOnDemand,
											OS: e.osMobileString || e.getOS(),
											Browser: e.browserMobileString || e.getBrowser(),
											StreamProto: e.protocol,
											StartUpTime: e.startTime,
											Origin: e.origin,
											Content: e.content,
											Timezone: new Date().getTimezoneOffset(),
										},
									},
								})
							);
						}),
						(this.sendPlayerInfo = function () {
							e.eventInfo.next(
								new ot.manager.Message({
									Type: ot.manager.MessageType.MessageTypeEvent,
									ArgumentsEvent: {
										EventName: ot.manager.ArgumentsEvent.EventClass.PLAYER,
										Action: ot.manager.ArgumentsEvent.Actions.INFO,
										ArgumentsPlayerInfo: {
											PlayingState: e.state,
											WatchingTime: e.playingTime,
											BufferLength: e.bufferLength || -1,
											Rebuffers: e.rebuffers,
											RebufferingTime: e.reBufferingTime,
											BandwidthFluctuation: e.bandwidthFluctuation,
											Bandwidth: e.bandwidth,
										},
									},
								})
							);
						}),
						(this.sendPlayerState = function () {
							e.eventInfo.next(
								new ot.manager.Message({
									Type: ot.manager.MessageType.MessageTypeEvent,
									Timestamp: Date.now(),
									ArgumentsEvent: {
										EventName: ot.manager.ArgumentsEvent.EventClass.PLAYER,
										Action: ot.manager.ArgumentsEvent.Actions.STATE,
										ArgumentsPlayerState: {
											PlayingState: e.state,
											Quality: e.bandwidth,
											Timeshift: e.timeshift,
										},
									},
								})
							);
						}),
						(this.sendPeerState = function () {
							e.eventInfo.next(
								new ot.manager.Message({
									Type: ot.manager.MessageType.MessageTypeEvent,
									Timestamp: Date.now(),
									ArgumentsEvent: {
										EventName: ot.manager.ArgumentsEvent.EventClass.PEER,
										Action: ot.manager.ArgumentsEvent.Actions.STATE,
										ArgumentsPeerState: {
											WatchingTimeSec: e.playingTime,
											BufferLengthBytes: e.bufferLength,
											Rebuffers: e.rebuffers,
											RebufferingTime: e.reBufferingTime,
										},
									},
								})
							);
						}),
						(this.eventInfo = new E());
				},
				ut = n(11),
				ct = ot.manager.ArgumentsEvent.EventClass,
				lt = ot.manager.ArgumentsEvent.Actions,
				ft = (function () {
					function e(e, t, n, r, i, o, s, a, u, c) {
						var l = this;
						(this.libVersion = "notset"),
							(this.startupTimeReported = !1),
							(this.initQuality = 0),
							(this.changedQuality = 0),
							(this.countChunks = 0),
							(this.qualityArray = [0, 0, 0, 0, 0, 0]),
							(this.setLibVersion = function (e) {
								return (l.libVersion = e), l;
							}),
							(this.start = function (e) {
								return l.statsReporter.restartReportLoop(e), l;
							}),
							(this.stop = function () {
								return l.statsReporter.stopReportLoop(), l;
							}),
							(this.next = function (e) {
								if (!e.ArgumentsEvent)
									return console.warn("empty event is sent.."), !1;
								if (e.ArgumentsEvent.EventName === ct.SWARM) {
									var t = e.ArgumentsEvent.ArgumentsSwarmSizeUpdate.Reason;
									if (null != t)
										switch (t) {
											case ot.manager.SwarmChangeReason.CONNECTED:
												l.statsReporter.incrementP2PEvents("connected");
												break;
											case ot.manager.SwarmChangeReason.DISCONNECTED:
												l.statsReporter.incrementP2PEvents("disconnect");
												break;
											case ot.manager.SwarmChangeReason.CONNECTERR:
												l.statsReporter.incrementP2PEvents("connect_err");
												break;
											case ot.manager.SwarmChangeReason.PINGPONG:
												l.statsReporter.incrementP2PEvents("pingpong");
												break;
											case ot.manager.SwarmChangeReason.CHANNELSWITCH:
												l.statsReporter.incrementP2PEvents("chn_switch");
										}
								}
								if (
									!l.startupTimeReported &&
									e.ArgumentsEvent.EventName === ct.PEER &&
									e.ArgumentsEvent.Action === lt.INFO
								)
									return (
										!!e.ArgumentsEvent.ArgumentsPeerInfo.StartUpTime &&
										((l.startupTimeReported = !0),
										l.statsReporter.reportQoE(
											new ut.QoEStats({
												startupTime:
													1e3 * e.ArgumentsEvent.ArgumentsPeerInfo.StartUpTime,
											})
										),
										!0)
									);
								if (
									e.ArgumentsEvent.EventName == ct.PINGPONG &&
									e.ArgumentsEvent.Action == lt.EXCHANGE
								) {
									var n = e.ArgumentsEvent.ArgumentsPingPongExchange,
										r = n.End - n.Start;
									l.statsReporter.reportDelay(n.Pid, r);
								}
								if (
									e.ArgumentsEvent.EventName === ct.PLAYER &&
									e.ArgumentsEvent.Action === lt.INFO
								) {
									l.statsReporter.reportQoE(
										new ut.QoEStats({
											bufferLength:
												e.ArgumentsEvent.ArgumentsPlayerInfo.BufferLength,
											rebufferTime:
												e.ArgumentsEvent.ArgumentsPlayerInfo.RebufferingTime,
											rebufferCnt:
												e.ArgumentsEvent.ArgumentsPlayerInfo.Rebuffers,
										})
									);
									var i = 0,
										o = 0;
									return (
										e.ArgumentsEvent.ArgumentsPlayerInfo.Bandwidth !==
											l.initQuality &&
											((l.changedQuality =
												e.ArgumentsEvent.ArgumentsPlayerInfo.Bandwidth),
											l.initQuality > l.changedQuality ? (i += 1) : (o += 1),
											l.statsReporter.setQualitySwitches(i, o),
											(l.countChunks = 0),
											(l.initQuality = l.changedQuality)),
										!0
									);
								}
								return (
									e.ArgumentsEvent.EventName === ct.RESOURCE
										? l.processResourceExchange(e)
										: e.ArgumentsEvent.EventName === ct.PEER &&
										  e.ArgumentsEvent.Action === lt.REGISTERED &&
										  l.processPeerRegistered(e),
									!0
								);
							}),
							(this.statsReporter = Object(ut.newStatsReporter)(
								e,
								t,
								n,
								r,
								i,
								"err:no_pid",
								o,
								s,
								a,
								c,
								void 0,
								u
							));
					}
					return (
						(e.prototype.processResourceExchange = function (e) {
							var t,
								n,
								r = "cdn";
							switch (e.ArgumentsEvent.Action) {
								case lt.DOWNLOADED:
									"v2v" === e.ArgumentsEvent.ArgumentsResourceDownloaded.Mode &&
										((r = "p2p"),
										((t = e.ArgumentsEvent.RemotePeerID) && "" !== t) ||
											(console.warn(
												"pid2 is not available for the peer p2p download"
											),
											(t = "err:no_pid2"))),
										(n =
											0 == this.initQuality
												? this.initQuality + 1
												: this.initQuality);
									var i = this.incrementCntChunks();
									this.qualityArray.splice(this.initQuality, n, i);
									var o =
											e.ArgumentsEvent.ArgumentsResourceDownloaded.SizeBytes,
										s =
											e.ArgumentsEvent.ArgumentsResourceDownloaded.TimeSpentMs;
									this.statsReporter.reportExchange(o, s, r, t),
										this.statsReporter.setQualityChunks(this.qualityArray),
										this.p2pStatsStore.addDownload(
											o,
											s,
											e.ArgumentsEvent.ArgumentsResourceDownloaded.Mode
										);
									break;
								case lt.UPLOADED:
									(r = "p2p_upload"),
										((t = e.ArgumentsEvent.RemotePeerID) && "" !== t) ||
											(console.warn(
												"pid2 is not available for the peer p2p download"
											),
											(t = "err:no_pid2")),
										this.statsReporter.reportExchange(
											e.ArgumentsEvent.ArgumentsResourceUploaded.SizeBytes,
											e.ArgumentsEvent.ArgumentsResourceUploaded.TimeSpentMs,
											r,
											t
										);
									break;
								case lt.AVAILABILITY:
									this.statsReporter.reportResourceAvailability(
										e.ArgumentsEvent.ArgumentsResourceAvailability.Pids,
										e.ArgumentsEvent.ArgumentsResourceAvailability.URL
									);
							}
						}),
						(e.prototype.processPeerRegistered = function (e) {
							(this.pid = e.ArgumentsEvent.ArgumentsRegistered.ID),
								(this.statsReporter.agentInfo.pid = this.pid);
						}),
						(e.prototype.incrementCntChunks = function () {
							for (var e = 0; e < this.qualityArray.length; e++)
								void 0 === this.statsReporter.qoeStats.qualityChkCnt[e] &&
									this.qualityArray.splice(e, e, 0);
							for (e = 0; e < this.qualityArray.length; e++)
								if (e === this.initQuality)
									return (
										void 0 === this.statsReporter.qoeStats.qualityChkCnt[e]
											? (this.countChunks = 1)
											: (this.countChunks =
													this.statsReporter.qoeStats.qualityChkCnt[e] + 1),
										this.countChunks
									);
						}),
						e
					);
				})(),
				pt = n(23),
				ht = n(4),
				gt = (function () {
					function e(e, t) {
						var n = this;
						void 0 === t && (t = 3e4),
							(this.cdnCount = 0),
							(this.v2vCount = 0),
							(this.statsDownload = [0, 0, 0, 0, 0.1, 0.1]),
							(this.sentCount = 0),
							(this.swarmSize = 0),
							(this.cdnCountLastSend = 0),
							(this.v2vCountLastSend = 0),
							(this.chunksLength = 0),
							(this.statsInterval = 3e4),
							(this.occupiedSlots = 0),
							(this.occupiedSlotsConst = 3),
							(this.occupiedSlotsCounter = 1),
							(this.next = function (e) {
								if (
									e.Type === ot.manager.MessageType.MessageTypeEvent &&
									(e.ArgumentsEvent.EventName ===
										ot.manager.ArgumentsEvent.EventClass.PEER &&
										e.ArgumentsEvent.Action ===
											ot.manager.ArgumentsEvent.Actions.REGISTERED &&
										e.ArgumentsEvent.ArgumentsRegistered &&
										(n.id = e.ArgumentsEvent.ArgumentsRegistered.ID),
									e.ArgumentsEvent.EventName ===
										ot.manager.ArgumentsEvent.EventClass.PLAYER &&
										e.ArgumentsEvent.Action ===
											ot.manager.ArgumentsEvent.Actions.INFO &&
										e.ArgumentsEvent.ArgumentsPlayerInfo &&
										(n.playerInfo = new ot.manager.ArgumentsPlayerInfo(
											e.ArgumentsEvent.ArgumentsPlayerInfo
										)),
									e.ArgumentsEvent.EventName ===
										ot.manager.ArgumentsEvent.EventClass.PEER &&
										e.ArgumentsEvent.Action ===
											ot.manager.ArgumentsEvent.Actions.INFO &&
										e.ArgumentsEvent.ArgumentsPeerInfo &&
										(n.peerInfo = new ot.manager.ArgumentsPeerInfo(
											e.ArgumentsEvent.ArgumentsPeerInfo
										)),
									e.ArgumentsEvent.EventName ===
										ot.manager.ArgumentsEvent.EventClass.SWARM &&
										e.ArgumentsEvent.Action ===
											ot.manager.ArgumentsEvent.Actions.SIZEUPDATE &&
										(n.swarmSize =
											e.ArgumentsEvent.ArgumentsSwarmSizeUpdate.Size),
									e.ArgumentsEvent.EventName ===
										ot.manager.ArgumentsEvent.EventClass.RESOURCE &&
										e.ArgumentsEvent.Action ===
											ot.manager.ArgumentsEvent.Actions.SLOTUPDATE &&
										((n.occupiedSlots =
											n.occupiedSlots +
											e.ArgumentsEvent.ArgumentsSlotUpdate.OccupiedSlot),
										n.occupiedSlotsCounter++),
									e.ArgumentsEvent.EventName ===
										ot.manager.ArgumentsEvent.EventClass.RESOURCE)
								)
									switch (e.ArgumentsEvent.Action) {
										case ot.manager.ArgumentsEvent.Actions.DOWNLOADED:
											"v2v" ===
											e.ArgumentsEvent.ArgumentsResourceDownloaded.Mode
												? ((n.v2vCount += 1),
												  n.statsDownload[0]++,
												  (n.statsDownload[2] +=
														e.ArgumentsEvent.ArgumentsResourceDownloaded.SizeBytes),
												  (n.statsDownload[4] +=
														e.ArgumentsEvent.ArgumentsResourceDownloaded.TimeSpentMs))
												: ((n.cdnCount += 1),
												  n.statsDownload[1]++,
												  (n.statsDownload[3] +=
														e.ArgumentsEvent.ArgumentsResourceDownloaded.SizeBytes),
												  (n.statsDownload[5] +=
														e.ArgumentsEvent.ArgumentsResourceDownloaded.TimeSpentMs)),
												(n.chunksLength +=
													e.ArgumentsEvent.ArgumentsResourceDownloaded.SizeBytes),
												Object(ht.c)(
													"V2V: " +
														n.statsDownload[0] +
														" - " +
														Math.round(
															n.statsDownload[2] / n.statsDownload[4]
														) +
														" KB/S | CDN: " +
														n.statsDownload[1] +
														" - " +
														Math.round(
															n.statsDownload[3] / n.statsDownload[5]
														) +
														" KB/S | SENT: " +
														n.sentCount
												);
											break;
										case ot.manager.ArgumentsEvent.Actions.UPLOADED:
											n.sentCount += 1;
									}
							}),
							(this.start = function () {
								return (
									(n.idInterval = setInterval(function () {
										n.sendMetrics(n.peerInfo, n.playerInfo);
									}, n.statsInterval)),
									n
								);
							}),
							(this.sendMetrics = function (e, t) {
								if (t)
									if (e) {
										var r = {
											id: n.id,
											IDContenu: e.Content,
											metrics: n.getMetricsString(e, t),
											os: e.OS,
											b: e.Browser,
											r: e.Radio ? "t" : "f",
											vod: e.VOD ? "t" : "f",
										};
										void 0 !== e.Origin && (r.or = e.Origin),
											void 0 !== t.BandwidthFluctuation &&
												(r.nf = t.BandwidthFluctuation.toString()),
											void 0 !== t.Bandwidth && (r.pq = t.Bandwidth.toString()),
											fetch(n.statsReceiverURL + "/?" + Object(pt.stringify)(r))
												.catch(function (e) {
													Object(ht.d)(
														"stats-receiver",
														"Could not send statistics: " + e
													);
												})
												.then(function () {
													(n.cdnCountLastSend = n.cdnCount),
														(n.v2vCountLastSend = n.v2vCount),
														(n.sentCount = 0),
														(n.occupiedSlots = 0),
														(n.occupiedSlotsCounter = 1);
												});
									} else
										Object(ht.d)("stats-receiver", "peerInfo not available");
								else Object(ht.d)("stats-receiver", "playerInfo not available");
							}),
							(this.statsReceiverURL = e),
							(this.statsInterval = t);
					}
					return (
						(e.prototype.stop = function () {
							clearInterval(this.idInterval);
						}),
						(e.prototype.getMetricsString = function (e, t) {
							return [
								e.StreamProto,
								"on",
								"" + this.sentCount,
								"" + this.swarmSize,
								this.getV2VRatio(),
								this.getOccupiedSlots(),
								this.roundValue(t.BufferLength),
								t.PlayingState.toString(),
								this.roundValue(
									this.chunksLength / (this.statsInterval / 1e3) / 1e3
								),
								this.roundValue(e.StartUpTime),
								"" + t.WatchingTime,
								this.roundValue(t.RebufferingTime),
								"" + t.Rebuffers,
								this.getAudioAverageLength(),
								this.getVideoAverageLength(),
								this.getChunkCountValue(),
							].join("~");
						}),
						(e.prototype.roundValue = function (e) {
							return (Math.round(1e3 * e) / 1e3).toString();
						}),
						(e.prototype.getChunkCountValue = function () {
							var e = new Uint8Array(4),
								t = this.v2vCount - this.v2vCountLastSend,
								n = this.cdnCount - this.cdnCountLastSend;
							return (
								this.peerInfo.Radio
									? ((e[0] = Math.min(n, 256)),
									  (e[1] = Math.min(t, 256)),
									  (e[2] = 0),
									  (e[3] = 0))
									: ((e[0] = 0),
									  (e[1] = 0),
									  (e[2] = Math.min(n, 256)),
									  (e[3] = Math.min(t, 256))),
								new DataView(e.buffer).getInt32(0, !1).toString()
							);
						}),
						(e.prototype.getV2VRatio = function () {
							return 0 === this.v2vCount && 0 === this.cdnCount
								? "0"
								: Math.round(
										this.v2vCount / (this.v2vCount + this.cdnCount)
								  ).toString();
						}),
						(e.prototype.getAudioAverageLength = function () {
							return this.peerInfo.Radio
								? Math.round(
										this.chunksLength / (this.v2vCount + this.cdnCount)
								  ).toString()
								: "0";
						}),
						(e.prototype.getVideoAverageLength = function () {
							return this.peerInfo.Radio
								? "0"
								: Math.round(
										this.chunksLength / (this.v2vCount + this.cdnCount)
								  ).toString();
						}),
						(e.prototype.getOccupiedSlots = function () {
							return (
								this.occupiedSlotsCounter > 1 &&
									(this.occupiedSlotsCounter = this.occupiedSlotsCounter - 1),
								Math.round(
									this.occupiedSlots / this.occupiedSlotsCounter
								).toString()
							);
						}),
						e
					);
				})(),
				dt = (function () {
					function e() {
						(this.readyState = 0),
							(this.timeout = 1e4),
							(this.withCredentials = !1),
							(this.DONE = 4),
							(this.HEADERS_RECEIVED = 2),
							(this.LOADING = 3),
							(this.OPENED = 1),
							(this.UNSENT = 0),
							(this.timeoutBeforeSend = 50),
							(this.onreadystatechange = function () {});
					}
					return (
						(e.prototype.abort = function () {
							clearTimeout(this.timeoutID);
						}),
						(e.prototype.getAllResponseHeaders = function () {
							return (
								Object(ht.d)(
									"ebxhr",
									"getAllResponseHeaders method is not supported by current version"
								),
								""
							);
						}),
						(e.prototype.getResponseHeader = function (e) {
							return "";
						}),
						(e.prototype.open = function (e, t, n, r, i) {
							if (!this.resourceManager)
								throw new Error("Resource Manager is not bound");
							if ("GET" !== e) throw new Error("Only GET is allowed");
							if (!t) throw new Error("Url should be set to send a request");
							(this.responseURL = t),
								(this.readyState = 1),
								this.onreadystatechange && this.onreadystatechange({});
						}),
						(e.prototype.overrideMimeType = function (e) {
							throw new Error("Method not implemented.");
						}),
						(e.prototype.send = function (e) {
							var t = this;
							(this.requestTime = Date.now()),
								(this.timeoutID = setTimeout(function () {
									clearTimeout(t.timeoutID),
										t.resourceManager
											.getResource(t.responseURL, t.timeout)
											.then(function (e) {
												setTimeout(function () {
													var n = e.buffer;
													(t.response = n),
														(t.readyState = 4),
														(t.status = 200),
														(t.statusText = "OK"),
														(t.responseTime = Date.now()),
														t.onreadystatechange && t.onreadystatechange({}),
														t.onload &&
															t.onload({
																lengthComputable: !0,
																loaded: e.byteLength,
																total: e.byteLength,
															});
												}, 0);
											})
											.catch(function (e) {
												t.onerror &&
													((t.status = 409),
													(t.statusText = "OK"),
													(t.responseTime = Date.now()),
													t.onreadystatechange && t.onreadystatechange({}),
													t.onerror({
														lengthComputable: !0,
														loaded: 0,
														total: 0,
													}));
											})
											.finally(function () {
												t.onloadend && t.onloadend({});
											});
								}, this.timeoutBeforeSend));
						}),
						(e.prototype.setRequestHeader = function (e, t) {
							Object(ht.d)("ebxhr", "SetRequestHeader Method not implemented.");
						}),
						(e.prototype.addEventListener = function (e, t, n) {}),
						(e.prototype.removeEventListener = function (e, t, n) {
							throw new Error("Method not implemented.");
						}),
						(e.prototype.dispatchEvent = function (e) {
							throw new Error("Method not implemented.");
						}),
						(e.prototype.bindResourceManager = function (e) {
							return (this.resourceManager = e), this;
						}),
						(e.prototype.setTimeoutBeforeSend = function (e) {
							return (this.timeoutBeforeSend = e), this;
						}),
						e
					);
				})(),
				yt = (function (e) {
					function t(t, n) {
						var r = e.call(this, t, n) || this;
						return (r.scheduler = t), (r.work = n), r;
					}
					return (
						i(t, e),
						(t.prototype.schedule = function (t, n) {
							return (
								void 0 === n && (n = 0),
								n > 0
									? e.prototype.schedule.call(this, t, n)
									: ((this.delay = n),
									  (this.state = t),
									  this.scheduler.flush(this),
									  this)
							);
						}),
						(t.prototype.execute = function (t, n) {
							return n > 0 || this.closed
								? e.prototype.execute.call(this, t, n)
								: this._execute(t, n);
						}),
						(t.prototype.requestAsyncId = function (t, n, r) {
							return (
								void 0 === r && (r = 0),
								(null !== r && r > 0) || (null === r && this.delay > 0)
									? e.prototype.requestAsyncId.call(this, t, n, r)
									: t.flush(this)
							);
						}),
						t
					);
				})(Z),
				mt = new ((function (e) {
					function t() {
						return (null !== e && e.apply(this, arguments)) || this;
					}
					return i(t, e), t;
				})(te))(yt),
				bt = new A(function (e) {
					return e.complete();
				});
			function wt(e) {
				return e
					? (function (e) {
							return new A(function (t) {
								return e.schedule(function () {
									return t.complete();
								});
							});
					  })(e)
					: bt;
			}
			function St() {
				for (var e = [], t = 0; t < arguments.length; t++) e[t] = arguments[t];
				var n = e[e.length - 1];
				return ge(n) ? (e.pop(), W(e, n)) : ye(e);
			}
			function Pt(e, t) {
				return new A(
					t
						? function (n) {
								return t.schedule(vt, 0, { error: e, subscriber: n });
						  }
						: function (t) {
								return t.error(e);
						  }
				);
			}
			function vt(e) {
				var t = e.error;
				e.subscriber.error(t);
			}
			st || (st = {});
			var At = (function () {
				function e(e, t, n) {
					(this.kind = e),
						(this.value = t),
						(this.error = n),
						(this.hasValue = "N" === e);
				}
				return (
					(e.prototype.observe = function (e) {
						switch (this.kind) {
							case "N":
								return e.next && e.next(this.value);
							case "E":
								return e.error && e.error(this.error);
							case "C":
								return e.complete && e.complete();
						}
					}),
					(e.prototype.do = function (e, t, n) {
						switch (this.kind) {
							case "N":
								return e && e(this.value);
							case "E":
								return t && t(this.error);
							case "C":
								return n && n();
						}
					}),
					(e.prototype.accept = function (e, t, n) {
						return e && "function" == typeof e.next
							? this.observe(e)
							: this.do(e, t, n);
					}),
					(e.prototype.toObservable = function () {
						switch (this.kind) {
							case "N":
								return St(this.value);
							case "E":
								return Pt(this.error);
							case "C":
								return wt();
						}
						throw new Error("unexpected notification kind value");
					}),
					(e.createNext = function (t) {
						return void 0 !== t ? new e("N", t) : e.undefinedValueNotification;
					}),
					(e.createError = function (t) {
						return new e("E", void 0, t);
					}),
					(e.createComplete = function () {
						return e.completeNotification;
					}),
					(e.completeNotification = new e("C")),
					(e.undefinedValueNotification = new e("N", void 0)),
					e
				);
			})();
			var Ot = (function (e) {
					function t(t, n, r) {
						void 0 === r && (r = 0);
						var i = e.call(this, t) || this;
						return (i.scheduler = n), (i.delay = r), i;
					}
					return (
						i(t, e),
						(t.dispatch = function (e) {
							var t = e.notification,
								n = e.destination;
							t.observe(n), this.unsubscribe();
						}),
						(t.prototype.scheduleMessage = function (e) {
							this.destination.add(
								this.scheduler.schedule(
									t.dispatch,
									this.delay,
									new Tt(e, this.destination)
								)
							);
						}),
						(t.prototype._next = function (e) {
							this.scheduleMessage(At.createNext(e));
						}),
						(t.prototype._error = function (e) {
							this.scheduleMessage(At.createError(e)), this.unsubscribe();
						}),
						(t.prototype._complete = function () {
							this.scheduleMessage(At.createComplete()), this.unsubscribe();
						}),
						t
					);
				})(m),
				Tt = (function () {
					return function (e, t) {
						(this.notification = e), (this.destination = t);
					};
				})(),
				Ct = (function (e) {
					function t(t, n, r) {
						void 0 === t && (t = Number.POSITIVE_INFINITY),
							void 0 === n && (n = Number.POSITIVE_INFINITY);
						var i = e.call(this) || this;
						return (
							(i.scheduler = r),
							(i._events = []),
							(i._infiniteTimeWindow = !1),
							(i._bufferSize = t < 1 ? 1 : t),
							(i._windowTime = n < 1 ? 1 : n),
							n === Number.POSITIVE_INFINITY
								? ((i._infiniteTimeWindow = !0),
								  (i.next = i.nextInfiniteTimeWindow))
								: (i.next = i.nextTimeWindow),
							i
						);
					}
					return (
						i(t, e),
						(t.prototype.nextInfiniteTimeWindow = function (t) {
							if (!this.isStopped) {
								var n = this._events;
								n.push(t), n.length > this._bufferSize && n.shift();
							}
							e.prototype.next.call(this, t);
						}),
						(t.prototype.nextTimeWindow = function (t) {
							this.isStopped ||
								(this._events.push(new Rt(this._getNow(), t)),
								this._trimBufferThenGetEvents()),
								e.prototype.next.call(this, t);
						}),
						(t.prototype._subscribe = function (e) {
							var t,
								n = this._infiniteTimeWindow,
								r = n ? this._events : this._trimBufferThenGetEvents(),
								i = this.scheduler,
								o = r.length;
							if (this.closed) throw new T();
							if (
								(this.isStopped || this.hasError
									? (t = g.EMPTY)
									: (this.observers.push(e), (t = new C(this, e))),
								i && e.add((e = new Ot(e, i))),
								n)
							)
								for (var s = 0; s < o && !e.closed; s++) e.next(r[s]);
							else for (s = 0; s < o && !e.closed; s++) e.next(r[s].value);
							return (
								this.hasError
									? e.error(this.thrownError)
									: this.isStopped && e.complete(),
								t
							);
						}),
						(t.prototype._getNow = function () {
							return (this.scheduler || mt).now();
						}),
						(t.prototype._trimBufferThenGetEvents = function () {
							for (
								var e = this._getNow(),
									t = this._bufferSize,
									n = this._windowTime,
									r = this._events,
									i = r.length,
									o = 0;
								o < i && !(e - r[o].time < n);

							)
								o++;
							return (
								i > t && (o = Math.max(o, i - t)), o > 0 && r.splice(0, o), r
							);
						}),
						t
					);
				})(E),
				Rt = (function () {
					return function (e, t) {
						(this.time = e), (this.value = t);
					};
				})(),
				Et = {
					url: "",
					deserializer: function (e) {
						return JSON.parse(e.data);
					},
					serializer: function (e) {
						return JSON.stringify(e);
					},
				},
				Mt = (function (e) {
					function t(t, n) {
						var r = e.call(this) || this;
						if (t instanceof A) (r.destination = n), (r.source = t);
						else {
							var i = (r._config = o({}, Et));
							if (((r._output = new E()), "string" == typeof t)) i.url = t;
							else for (var s in t) t.hasOwnProperty(s) && (i[s] = t[s]);
							if (!i.WebSocketCtor && WebSocket) i.WebSocketCtor = WebSocket;
							else if (!i.WebSocketCtor)
								throw new Error("no WebSocket constructor can be found");
							r.destination = new Ct();
						}
						return r;
					}
					return (
						i(t, e),
						(t.prototype.lift = function (e) {
							var n = new t(this._config, this.destination);
							return (n.operator = e), (n.source = this), n;
						}),
						(t.prototype._resetState = function () {
							(this._socket = null),
								this.source || (this.destination = new Ct()),
								(this._output = new E());
						}),
						(t.prototype.multiplex = function (e, t, n) {
							var r = this;
							return new A(function (i) {
								try {
									r.next(e());
								} catch (e) {
									i.error(e);
								}
								var o = r.subscribe(
									function (e) {
										try {
											n(e) && i.next(e);
										} catch (e) {
											i.error(e);
										}
									},
									function (e) {
										return i.error(e);
									},
									function () {
										return i.complete();
									}
								);
								return function () {
									try {
										r.next(t());
									} catch (e) {
										i.error(e);
									}
									o.unsubscribe();
								};
							});
						}),
						(t.prototype._connectSocket = function () {
							var e = this,
								t = this._config,
								n = t.WebSocketCtor,
								r = t.protocol,
								i = t.url,
								o = t.binaryType,
								s = this._output,
								a = null;
							try {
								(a = r ? new n(i, r) : new n(i)),
									(this._socket = a),
									o && (this._socket.binaryType = o);
							} catch (e) {
								return void s.error(e);
							}
							var u = new g(function () {
								(e._socket = null), a && 1 === a.readyState && a.close();
							});
							(a.onopen = function (t) {
								if (!e._socket) return a.close(), void e._resetState();
								var n = e._config.openObserver;
								n && n.next(t);
								var r = e.destination;
								(e.destination = m.create(
									function (t) {
										if (1 === a.readyState)
											try {
												var n = e._config.serializer;
												a.send(n(t));
											} catch (t) {
												e.destination.error(t);
											}
									},
									function (t) {
										var n = e._config.closingObserver;
										n && n.next(void 0),
											t && t.code
												? a.close(t.code, t.reason)
												: s.error(
														new TypeError(
															"WebSocketSubject.error must be called with an object with an error code, and an optional reason: { code: number, reason: string }"
														)
												  ),
											e._resetState();
									},
									function () {
										var t = e._config.closingObserver;
										t && t.next(void 0), a.close(), e._resetState();
									}
								)),
									r && r instanceof Ct && u.add(r.subscribe(e.destination));
							}),
								(a.onerror = function (t) {
									e._resetState(), s.error(t);
								}),
								(a.onclose = function (t) {
									e._resetState();
									var n = e._config.closeObserver;
									n && n.next(t), t.wasClean ? s.complete() : s.error(t);
								}),
								(a.onmessage = function (t) {
									try {
										var n = e._config.deserializer;
										s.next(n(t));
									} catch (e) {
										s.error(e);
									}
								});
						}),
						(t.prototype._subscribe = function (e) {
							var t = this,
								n = this.source;
							return n
								? n.subscribe(e)
								: (this._socket || this._connectSocket(),
								  this._output.subscribe(e),
								  e.add(function () {
										var e = t._socket;
										0 === t._output.observers.length &&
											(e && 1 === e.readyState && e.close(), t._resetState());
								  }),
								  e);
						}),
						(t.prototype.unsubscribe = function () {
							var t = this._socket;
							t && 1 === t.readyState && t.close(),
								this._resetState(),
								e.prototype.unsubscribe.call(this);
						}),
						t
					);
				})(M);
			var Lt = Object(ht.a)("manager-connector");
			var xt = (function () {
					function e() {
						var e = this;
						(this.messageSubject = new E()),
							(this.stateChannel = new E()),
							(this.assign = function (t) {
								return (e.roomURL = t), (e.url = t), e;
							}),
							(this.reconnectIn = function (t) {
								return (e.reconnectInterval = t), e;
							}),
							(this.getBucketID = function () {
								return e.bucketId;
							}),
							(this.close = function () {
								e.rootSubscription && e.rootSubscription.unsubscribe(),
									e.conn && e.conn.complete(),
									e.toid && clearTimeout(e.toid);
							}),
							(this.next = function (t) {
								e.conn.isStopped
									? Lt.warn("connection is stopped, message not sent")
									: e.conn.next(t);
							}),
							(this.setID = function (t) {
								return (
									(e.id = t),
									(e.url = e.roomURL + "/" + e.id),
									(e.bucketId = (function (e, t) {
										for (
											var n = e.split("-").reduce(function (e, t) {
													return e + t;
												}),
												r = 0,
												i = 0;
											i < n.length;
											i++
										)
											r += n.charCodeAt(i);
										return r % t;
									})(e.id, 2)),
									e
								);
							}),
							(this.notifyStateChanges = function (t) {
								return e.stateChannel.subscribe(t);
							}),
							(this.getID = function () {
								return e.id;
							}),
							(this.noID = function () {
								return (e.id = ""), (e.url = e.roomURL), e;
							}),
							(this.subscribe = function (t) {
								return e.messageSubject.subscribe(t);
							});
					}
					return (
						(e.session = function () {
							return new e().reconnectIn(2e3);
						}),
						(e.prototype.start = function () {
							var e,
								t = this;
							return (
								this.conn && (this.conn.complete(), (this.conn = void 0)),
								(this.conn =
									((e = {
										url: this.url,
										protocol: "easybroadcast.fr_2.0",
										binaryType: "arraybuffer",
										deserializer: function (e) {
											try {
												return ot.manager.Message.decode(
													new Uint8Array(e.data)
												);
											} catch (e) {
												return Lt.warn(e), null;
											}
										},
										serializer: function (e) {
											return ot.manager.Message.encode(e).finish();
										},
										openObserver: {
											next: function () {
												t.stateChannel.next("con");
											},
										},
										closeObserver: {
											next: function () {
												t.stateChannel.next("dis");
											},
										},
									}),
									new Mt(e))),
								this.rootSubscription && this.rootSubscription.unsubscribe(),
								(this.rootSubscription = this.conn.subscribe(
									function (e) {
										return t.messageSubject.next(e);
									},
									function (e) {
										Lt.info("Error getting message from WebSocket", e),
											(t.toid = setTimeout(function () {
												return t.start();
											}, t.reconnectInterval));
									},
									function () {
										Lt.info("websocket complet");
									}
								)),
								this
							);
						}),
						e
					);
				})(),
				Dt = n(1),
				It = n(2);
			var kt =
					It.Buffer.from &&
					It.Buffer.alloc &&
					It.Buffer.allocUnsafe &&
					It.Buffer.allocUnsafeSlow
						? It.Buffer.from
						: (e) => new It.Buffer(e),
				jt = function (e, t) {
					const n = (e, n) => t(e, n) >>> 0;
					return (n.signed = t), (n.unsigned = n), (n.model = e), n;
				};
			jt("crc1", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = ~~t,
					r = 0;
				for (let t = 0; t < e.length; t++) {
					r += e[t];
				}
				return (n += r % 256), n % 256;
			});
			let Bt = [
				0, 7, 14, 9, 28, 27, 18, 21, 56, 63, 54, 49, 36, 35, 42, 45, 112, 119,
				126, 121, 108, 107, 98, 101, 72, 79, 70, 65, 84, 83, 90, 93, 224, 231,
				238, 233, 252, 251, 242, 245, 216, 223, 214, 209, 196, 195, 202, 205,
				144, 151, 158, 153, 140, 139, 130, 133, 168, 175, 166, 161, 180, 179,
				186, 189, 199, 192, 201, 206, 219, 220, 213, 210, 255, 248, 241, 246,
				227, 228, 237, 234, 183, 176, 185, 190, 171, 172, 165, 162, 143, 136,
				129, 134, 147, 148, 157, 154, 39, 32, 41, 46, 59, 60, 53, 50, 31, 24,
				17, 22, 3, 4, 13, 10, 87, 80, 89, 94, 75, 76, 69, 66, 111, 104, 97, 102,
				115, 116, 125, 122, 137, 142, 135, 128, 149, 146, 155, 156, 177, 182,
				191, 184, 173, 170, 163, 164, 249, 254, 247, 240, 229, 226, 235, 236,
				193, 198, 207, 200, 221, 218, 211, 212, 105, 110, 103, 96, 117, 114,
				123, 124, 81, 86, 95, 88, 77, 74, 67, 68, 25, 30, 23, 16, 5, 2, 11, 12,
				33, 38, 47, 40, 61, 58, 51, 52, 78, 73, 64, 71, 82, 85, 92, 91, 118,
				113, 120, 127, 106, 109, 100, 99, 62, 57, 48, 55, 34, 37, 44, 43, 6, 1,
				8, 15, 26, 29, 20, 19, 174, 169, 160, 167, 178, 181, 188, 187, 150, 145,
				152, 159, 138, 141, 132, 131, 222, 217, 208, 215, 194, 197, 204, 203,
				230, 225, 232, 239, 250, 253, 244, 243,
			];
			"undefined" != typeof Int32Array && (Bt = new Int32Array(Bt));
			jt("crc-8", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = ~~t;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 255 & Bt[255 & (n ^ r)];
				}
				return n;
			});
			let Nt = [
				0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
				157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
				35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
				190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
				70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
				219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
				101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
				248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
				140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147,
				205, 17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236,
				14, 80, 175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82,
				176, 238, 50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145,
				207, 45, 115, 202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105,
				55, 213, 139, 87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119,
				244, 170, 72, 22, 233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151,
				201, 74, 20, 246, 168, 116, 42, 200, 150, 21, 75, 169, 247, 182, 232,
				10, 84, 215, 137, 107, 53,
			];
			"undefined" != typeof Int32Array && (Nt = new Int32Array(Nt));
			jt("dallas-1-wire", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = ~~t;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 255 & Nt[255 & (n ^ r)];
				}
				return n;
			});
			let Ut = [
				0, 49345, 49537, 320, 49921, 960, 640, 49729, 50689, 1728, 1920, 51009,
				1280, 50625, 50305, 1088, 52225, 3264, 3456, 52545, 3840, 53185, 52865,
				3648, 2560, 51905, 52097, 2880, 51457, 2496, 2176, 51265, 55297, 6336,
				6528, 55617, 6912, 56257, 55937, 6720, 7680, 57025, 57217, 8e3, 56577,
				7616, 7296, 56385, 5120, 54465, 54657, 5440, 55041, 6080, 5760, 54849,
				53761, 4800, 4992, 54081, 4352, 53697, 53377, 4160, 61441, 12480, 12672,
				61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721,
				13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281, 16320, 16e3,
				65089, 64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240,
				59585, 59777, 10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160,
				61249, 11520, 60865, 60545, 11328, 58369, 9408, 9600, 58689, 9984,
				59329, 59009, 9792, 8704, 58049, 58241, 9024, 57601, 8640, 8320, 57409,
				40961, 24768, 24960, 41281, 25344, 41921, 41601, 25152, 26112, 42689,
				42881, 26432, 42241, 26048, 25728, 42049, 27648, 44225, 44417, 27968,
				44801, 28608, 28288, 44609, 43521, 27328, 27520, 43841, 26880, 43457,
				43137, 26688, 30720, 47297, 47489, 31040, 47873, 31680, 31360, 47681,
				48641, 32448, 32640, 48961, 32e3, 48577, 48257, 31808, 46081, 29888,
				30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 29504,
				45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440,
				21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568,
				39937, 23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617,
				39809, 23360, 39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137,
				19200, 35777, 35457, 19008, 19968, 36545, 36737, 20288, 36097, 19904,
				19584, 35905, 17408, 33985, 34177, 17728, 34561, 18368, 18048, 34369,
				33281, 17088, 17280, 33601, 16640, 33217, 32897, 16448,
			];
			"undefined" != typeof Int32Array && (Ut = new Int32Array(Ut));
			var _t = jt("crc-16", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = ~~t;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 65535 & (Ut[255 & (n ^ r)] ^ (n >> 8));
				}
				return n;
			});
			let qt = [
				0, 4129, 8258, 12387, 16516, 20645, 24774, 28903, 33032, 37161, 41290,
				45419, 49548, 53677, 57806, 61935, 4657, 528, 12915, 8786, 21173, 17044,
				29431, 25302, 37689, 33560, 45947, 41818, 54205, 50076, 62463, 58334,
				9314, 13379, 1056, 5121, 25830, 29895, 17572, 21637, 42346, 46411,
				34088, 38153, 58862, 62927, 50604, 54669, 13907, 9842, 5649, 1584,
				30423, 26358, 22165, 18100, 46939, 42874, 38681, 34616, 63455, 59390,
				55197, 51132, 18628, 22757, 26758, 30887, 2112, 6241, 10242, 14371,
				51660, 55789, 59790, 63919, 35144, 39273, 43274, 47403, 23285, 19156,
				31415, 27286, 6769, 2640, 14899, 10770, 56317, 52188, 64447, 60318,
				39801, 35672, 47931, 43802, 27814, 31879, 19684, 23749, 11298, 15363,
				3168, 7233, 60846, 64911, 52716, 56781, 44330, 48395, 36200, 40265,
				32407, 28342, 24277, 20212, 15891, 11826, 7761, 3696, 65439, 61374,
				57309, 53244, 48923, 44858, 40793, 36728, 37256, 33193, 45514, 41451,
				53516, 49453, 61774, 57711, 4224, 161, 12482, 8419, 20484, 16421, 28742,
				24679, 33721, 37784, 41979, 46042, 49981, 54044, 58239, 62302, 689,
				4752, 8947, 13010, 16949, 21012, 25207, 29270, 46570, 42443, 38312,
				34185, 62830, 58703, 54572, 50445, 13538, 9411, 5280, 1153, 29798,
				25671, 21540, 17413, 42971, 47098, 34713, 38840, 59231, 63358, 50973,
				55100, 9939, 14066, 1681, 5808, 26199, 30326, 17941, 22068, 55628,
				51565, 63758, 59695, 39368, 35305, 47498, 43435, 22596, 18533, 30726,
				26663, 6336, 2273, 14466, 10403, 52093, 56156, 60223, 64286, 35833,
				39896, 43963, 48026, 19061, 23124, 27191, 31254, 2801, 6864, 10931,
				14994, 64814, 60687, 56684, 52557, 48554, 44427, 40424, 36297, 31782,
				27655, 23652, 19525, 15522, 11395, 7392, 3265, 61215, 65342, 53085,
				57212, 44955, 49082, 36825, 40952, 28183, 32310, 20053, 24180, 11923,
				16050, 3793, 7920,
			];
			"undefined" != typeof Int32Array && (qt = new Int32Array(qt));
			jt("ccitt", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = void 0 !== t ? ~~t : 65535;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 65535 & (qt[255 & ((n >> 8) ^ r)] ^ (n << 8));
				}
				return n;
			});
			let Vt = [
				0, 49345, 49537, 320, 49921, 960, 640, 49729, 50689, 1728, 1920, 51009,
				1280, 50625, 50305, 1088, 52225, 3264, 3456, 52545, 3840, 53185, 52865,
				3648, 2560, 51905, 52097, 2880, 51457, 2496, 2176, 51265, 55297, 6336,
				6528, 55617, 6912, 56257, 55937, 6720, 7680, 57025, 57217, 8e3, 56577,
				7616, 7296, 56385, 5120, 54465, 54657, 5440, 55041, 6080, 5760, 54849,
				53761, 4800, 4992, 54081, 4352, 53697, 53377, 4160, 61441, 12480, 12672,
				61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721,
				13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281, 16320, 16e3,
				65089, 64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240,
				59585, 59777, 10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160,
				61249, 11520, 60865, 60545, 11328, 58369, 9408, 9600, 58689, 9984,
				59329, 59009, 9792, 8704, 58049, 58241, 9024, 57601, 8640, 8320, 57409,
				40961, 24768, 24960, 41281, 25344, 41921, 41601, 25152, 26112, 42689,
				42881, 26432, 42241, 26048, 25728, 42049, 27648, 44225, 44417, 27968,
				44801, 28608, 28288, 44609, 43521, 27328, 27520, 43841, 26880, 43457,
				43137, 26688, 30720, 47297, 47489, 31040, 47873, 31680, 31360, 47681,
				48641, 32448, 32640, 48961, 32e3, 48577, 48257, 31808, 46081, 29888,
				30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 29504,
				45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440,
				21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568,
				39937, 23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617,
				39809, 23360, 39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137,
				19200, 35777, 35457, 19008, 19968, 36545, 36737, 20288, 36097, 19904,
				19584, 35905, 17408, 33985, 34177, 17728, 34561, 18368, 18048, 34369,
				33281, 17088, 17280, 33601, 16640, 33217, 32897, 16448,
			];
			"undefined" != typeof Int32Array && (Vt = new Int32Array(Vt));
			jt("crc-16-modbus", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = void 0 !== t ? ~~t : 65535;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 65535 & (Vt[255 & (n ^ r)] ^ (n >> 8));
				}
				return n;
			});
			jt("xmodem", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = void 0 !== t ? ~~t : 0;
				for (let t = 0; t < e.length; t++) {
					let r = (n >>> 8) & 255;
					(r ^= 255 & e[t]),
						(r ^= r >>> 4),
						(n = (n << 8) & 65535),
						(n ^= r),
						(r = (r << 5) & 65535),
						(n ^= r),
						(r = (r << 7) & 65535),
						(n ^= r);
				}
				return n;
			});
			let Ft = [
				0, 4489, 8978, 12955, 17956, 22445, 25910, 29887, 35912, 40385, 44890,
				48851, 51820, 56293, 59774, 63735, 4225, 264, 13203, 8730, 22181, 18220,
				30135, 25662, 40137, 36160, 49115, 44626, 56045, 52068, 63999, 59510,
				8450, 12427, 528, 5017, 26406, 30383, 17460, 21949, 44362, 48323, 36440,
				40913, 60270, 64231, 51324, 55797, 12675, 8202, 4753, 792, 30631, 26158,
				21685, 17724, 48587, 44098, 40665, 36688, 64495, 60006, 55549, 51572,
				16900, 21389, 24854, 28831, 1056, 5545, 10034, 14011, 52812, 57285,
				60766, 64727, 34920, 39393, 43898, 47859, 21125, 17164, 29079, 24606,
				5281, 1320, 14259, 9786, 57037, 53060, 64991, 60502, 39145, 35168,
				48123, 43634, 25350, 29327, 16404, 20893, 9506, 13483, 1584, 6073,
				61262, 65223, 52316, 56789, 43370, 47331, 35448, 39921, 29575, 25102,
				20629, 16668, 13731, 9258, 5809, 1848, 65487, 60998, 56541, 52564,
				47595, 43106, 39673, 35696, 33800, 38273, 42778, 46739, 49708, 54181,
				57662, 61623, 2112, 6601, 11090, 15067, 20068, 24557, 28022, 31999,
				38025, 34048, 47003, 42514, 53933, 49956, 61887, 57398, 6337, 2376,
				15315, 10842, 24293, 20332, 32247, 27774, 42250, 46211, 34328, 38801,
				58158, 62119, 49212, 53685, 10562, 14539, 2640, 7129, 28518, 32495,
				19572, 24061, 46475, 41986, 38553, 34576, 62383, 57894, 53437, 49460,
				14787, 10314, 6865, 2904, 32743, 28270, 23797, 19836, 50700, 55173,
				58654, 62615, 32808, 37281, 41786, 45747, 19012, 23501, 26966, 30943,
				3168, 7657, 12146, 16123, 54925, 50948, 62879, 58390, 37033, 33056,
				46011, 41522, 23237, 19276, 31191, 26718, 7393, 3432, 16371, 11898,
				59150, 63111, 50204, 54677, 41258, 45219, 33336, 37809, 27462, 31439,
				18516, 23005, 11618, 15595, 3696, 8185, 63375, 58886, 54429, 50452,
				45483, 40994, 37561, 33584, 31687, 27214, 22741, 18780, 15843, 11370,
				7921, 3960,
			];
			"undefined" != typeof Int32Array && (Ft = new Int32Array(Ft));
			jt("kermit", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = void 0 !== t ? ~~t : 0;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 65535 & (Ft[255 & (n ^ r)] ^ (n >> 8));
				}
				return n;
			});
			let zt = [
				0, 8801531, 9098509, 825846, 9692897, 1419802, 1651692, 10452759,
				10584377, 2608578, 2839604, 11344079, 3303384, 11807523, 12104405,
				4128302, 12930697, 4391538, 5217156, 13227903, 5679208, 13690003,
				14450021, 5910942, 6606768, 14844747, 15604413, 6837830, 16197969,
				7431594, 8256604, 16494759, 840169, 9084178, 8783076, 18463, 10434312,
				1670131, 1434117, 9678590, 11358416, 2825259, 2590173, 10602790,
				4109873, 12122826, 11821884, 3289031, 13213536, 5231515, 4409965,
				12912278, 5929345, 14431610, 13675660, 5693559, 6823513, 15618722,
				14863188, 6588335, 16513208, 8238147, 7417269, 16212302, 1680338,
				10481449, 9664223, 1391140, 9061683, 788936, 36926, 8838341, 12067563,
				4091408, 3340262, 11844381, 2868234, 11372785, 10555655, 2579964,
				14478683, 5939616, 5650518, 13661357, 5180346, 13190977, 12967607,
				4428364, 8219746, 16457881, 16234863, 7468436, 15633027, 6866552,
				6578062, 14816117, 1405499, 9649856, 10463030, 1698765, 8819930, 55329,
				803287, 9047340, 11858690, 3325945, 4072975, 12086004, 2561507,
				10574104, 11387118, 2853909, 13647026, 5664841, 5958079, 14460228,
				4446803, 12949160, 13176670, 5194661, 7454091, 16249200, 16476294,
				8201341, 14834538, 6559633, 6852199, 15647388, 3360676, 11864927,
				12161705, 4185682, 10527045, 2551230, 2782280, 11286707, 9619101,
				1346150, 1577872, 10379115, 73852, 8875143, 9172337, 899466, 16124205,
				7357910, 8182816, 16421083, 6680524, 14918455, 15678145, 6911546,
				5736468, 13747439, 14507289, 5968354, 12873461, 4334094, 5159928,
				13170435, 4167245, 12180150, 11879232, 3346363, 11301036, 2767959,
				2532769, 10545498, 10360692, 1596303, 1360505, 9604738, 913813, 9157998,
				8856728, 92259, 16439492, 8164415, 7343561, 16138546, 6897189, 15692510,
				14936872, 6662099, 5986813, 14488838, 13733104, 5750795, 13156124,
				5174247, 4352529, 12855018, 2810998, 11315341, 10498427, 2522496,
				12124823, 4148844, 3397530, 11901793, 9135439, 862644, 110658, 8912057,
				1606574, 10407765, 9590435, 1317464, 15706879, 6940164, 6651890,
				14889737, 8145950, 16384229, 16161043, 7394792, 5123014, 13133629,
				12910283, 4370992, 14535975, 5997020, 5707818, 13718737, 2504095,
				10516836, 11329682, 2796649, 11916158, 3383173, 4130419, 12143240,
				8893606, 129117, 876971, 9121104, 1331783, 9576124, 10389322, 1625009,
				14908182, 6633453, 6925851, 15721184, 7380471, 16175372, 16402682,
				8127489, 4389423, 12891860, 13119266, 5137369, 13704398, 5722165,
				6015427, 14517560,
			];
			"undefined" != typeof Int32Array && (zt = new Int32Array(zt));
			jt("crc-24", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = void 0 !== t ? ~~t : 11994318;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = 16777215 & (zt[255 & ((n >> 16) ^ r)] ^ (n << 8));
				}
				return n;
			});
			let Wt = [
				0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615,
				3915621685, 2657392035, 249268274, 2044508324, 3772115230, 2547177864,
				162941995, 2125561021, 3887607047, 2428444049, 498536548, 1789927666,
				4089016648, 2227061214, 450548861, 1843258603, 4107580753, 2211677639,
				325883990, 1684777152, 4251122042, 2321926636, 335633487, 1661365465,
				4195302755, 2366115317, 997073096, 1281953886, 3579855332, 2724688242,
				1006888145, 1258607687, 3524101629, 2768942443, 901097722, 1119000684,
				3686517206, 2898065728, 853044451, 1172266101, 3705015759, 2882616665,
				651767980, 1373503546, 3369554304, 3218104598, 565507253, 1454621731,
				3485111705, 3099436303, 671266974, 1594198024, 3322730930, 2970347812,
				795835527, 1483230225, 3244367275, 3060149565, 1994146192, 31158534,
				2563907772, 4023717930, 1907459465, 112637215, 2680153253, 3904427059,
				2013776290, 251722036, 2517215374, 3775830040, 2137656763, 141376813,
				2439277719, 3865271297, 1802195444, 476864866, 2238001368, 4066508878,
				1812370925, 453092731, 2181625025, 4111451223, 1706088902, 314042704,
				2344532202, 4240017532, 1658658271, 366619977, 2362670323, 4224994405,
				1303535960, 984961486, 2747007092, 3569037538, 1256170817, 1037604311,
				2765210733, 3554079995, 1131014506, 879679996, 2909243462, 3663771856,
				1141124467, 855842277, 2852801631, 3708648649, 1342533948, 654459306,
				3188396048, 3373015174, 1466479909, 544179635, 3110523913, 3462522015,
				1591671054, 702138776, 2966460450, 3352799412, 1504918807, 783551873,
				3082640443, 3233442989, 3988292384, 2596254646, 62317068, 1957810842,
				3939845945, 2647816111, 81470997, 1943803523, 3814918930, 2489596804,
				225274430, 2053790376, 3826175755, 2466906013, 167816743, 2097651377,
				4027552580, 2265490386, 503444072, 1762050814, 4150417245, 2154129355,
				426522225, 1852507879, 4275313526, 2312317920, 282753626, 1742555852,
				4189708143, 2394877945, 397917763, 1622183637, 3604390888, 2714866558,
				953729732, 1340076626, 3518719985, 2797360999, 1068828381, 1219638859,
				3624741850, 2936675148, 906185462, 1090812512, 3747672003, 2825379669,
				829329135, 1181335161, 3412177804, 3160834842, 628085408, 1382605366,
				3423369109, 3138078467, 570562233, 1426400815, 3317316542, 2998733608,
				733239954, 1555261956, 3268935591, 3050360625, 752459403, 1541320221,
				2607071920, 3965973030, 1969922972, 40735498, 2617837225, 3943577151,
				1913087877, 83908371, 2512341634, 3803740692, 2075208622, 213261112,
				2463272603, 3855990285, 2094854071, 198958881, 2262029012, 4057260610,
				1759359992, 534414190, 2176718541, 4139329115, 1873836001, 414664567,
				2282248934, 4279200368, 1711684554, 285281116, 2405801727, 4167216745,
				1634467795, 376229701, 2685067896, 3608007406, 1308918612, 956543938,
				2808555105, 3495958263, 1231636301, 1047427035, 2932959818, 3654703836,
				1088359270, 936918e3, 2847714899, 3736837829, 1202900863, 817233897,
				3183342108, 3401237130, 1404277552, 615818150, 3134207493, 3453421203,
				1423857449, 601450431, 3009837614, 3294710456, 1567103746, 711928724,
				3020668471, 3272380065, 1510334235, 755167117,
			];
			"undefined" != typeof Int32Array && (Wt = new Int32Array(Wt));
			jt("crc-32", function (e, t) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = 0 === t ? 0 : -1 ^ ~~t;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = Wt[255 & (n ^ r)] ^ (n >>> 8);
				}
				return -1 ^ n;
			});
			let Ht = [
				0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615,
				3915621685, 2657392035, 249268274, 2044508324, 3772115230, 2547177864,
				162941995, 2125561021, 3887607047, 2428444049, 498536548, 1789927666,
				4089016648, 2227061214, 450548861, 1843258603, 4107580753, 2211677639,
				325883990, 1684777152, 4251122042, 2321926636, 335633487, 1661365465,
				4195302755, 2366115317, 997073096, 1281953886, 3579855332, 2724688242,
				1006888145, 1258607687, 3524101629, 2768942443, 901097722, 1119000684,
				3686517206, 2898065728, 853044451, 1172266101, 3705015759, 2882616665,
				651767980, 1373503546, 3369554304, 3218104598, 565507253, 1454621731,
				3485111705, 3099436303, 671266974, 1594198024, 3322730930, 2970347812,
				795835527, 1483230225, 3244367275, 3060149565, 1994146192, 31158534,
				2563907772, 4023717930, 1907459465, 112637215, 2680153253, 3904427059,
				2013776290, 251722036, 2517215374, 3775830040, 2137656763, 141376813,
				2439277719, 3865271297, 1802195444, 476864866, 2238001368, 4066508878,
				1812370925, 453092731, 2181625025, 4111451223, 1706088902, 314042704,
				2344532202, 4240017532, 1658658271, 366619977, 2362670323, 4224994405,
				1303535960, 984961486, 2747007092, 3569037538, 1256170817, 1037604311,
				2765210733, 3554079995, 1131014506, 879679996, 2909243462, 3663771856,
				1141124467, 855842277, 2852801631, 3708648649, 1342533948, 654459306,
				3188396048, 3373015174, 1466479909, 544179635, 3110523913, 3462522015,
				1591671054, 702138776, 2966460450, 3352799412, 1504918807, 783551873,
				3082640443, 3233442989, 3988292384, 2596254646, 62317068, 1957810842,
				3939845945, 2647816111, 81470997, 1943803523, 3814918930, 2489596804,
				225274430, 2053790376, 3826175755, 2466906013, 167816743, 2097651377,
				4027552580, 2265490386, 503444072, 1762050814, 4150417245, 2154129355,
				426522225, 1852507879, 4275313526, 2312317920, 282753626, 1742555852,
				4189708143, 2394877945, 397917763, 1622183637, 3604390888, 2714866558,
				953729732, 1340076626, 3518719985, 2797360999, 1068828381, 1219638859,
				3624741850, 2936675148, 906185462, 1090812512, 3747672003, 2825379669,
				829329135, 1181335161, 3412177804, 3160834842, 628085408, 1382605366,
				3423369109, 3138078467, 570562233, 1426400815, 3317316542, 2998733608,
				733239954, 1555261956, 3268935591, 3050360625, 752459403, 1541320221,
				2607071920, 3965973030, 1969922972, 40735498, 2617837225, 3943577151,
				1913087877, 83908371, 2512341634, 3803740692, 2075208622, 213261112,
				2463272603, 3855990285, 2094854071, 198958881, 2262029012, 4057260610,
				1759359992, 534414190, 2176718541, 4139329115, 1873836001, 414664567,
				2282248934, 4279200368, 1711684554, 285281116, 2405801727, 4167216745,
				1634467795, 376229701, 2685067896, 3608007406, 1308918612, 956543938,
				2808555105, 3495958263, 1231636301, 1047427035, 2932959818, 3654703836,
				1088359270, 936918e3, 2847714899, 3736837829, 1202900863, 817233897,
				3183342108, 3401237130, 1404277552, 615818150, 3134207493, 3453421203,
				1423857449, 601450431, 3009837614, 3294710456, 1567103746, 711928724,
				3020668471, 3272380065, 1510334235, 755167117,
			];
			"undefined" != typeof Int32Array && (Ht = new Int32Array(Ht));
			jt("jam", function (e, t = -1) {
				It.Buffer.isBuffer(e) || (e = kt(e));
				let n = 0 === t ? 0 : ~~t;
				for (let t = 0; t < e.length; t++) {
					const r = e[t];
					n = Ht[255 & (n ^ r)] ^ (n >>> 8);
				}
				return n;
			});
			function Gt(e, t) {
				return function (n) {
					return n.lift(new Qt(e, t));
				};
			}
			var Qt = (function () {
					function e(e, t) {
						(this.predicate = e), (this.thisArg = t);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new Jt(e, this.predicate, this.thisArg));
						}),
						e
					);
				})(),
				Jt = (function (e) {
					function t(t, n, r) {
						var i = e.call(this, t) || this;
						return (i.predicate = n), (i.thisArg = r), (i.count = 0), i;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							var t;
							try {
								t = this.predicate.call(this.thisArg, e, this.count++);
							} catch (e) {
								return void this.destination.error(e);
							}
							t && this.destination.next(e);
						}),
						t
					);
				})(m);
			function Yt(e, t) {
				var n = !1;
				return (
					arguments.length >= 2 && (n = !0),
					function (r) {
						return r.lift(new Kt(e, t, n));
					}
				);
			}
			var Kt = (function () {
					function e(e, t, n) {
						void 0 === n && (n = !1),
							(this.accumulator = e),
							(this.seed = t),
							(this.hasSeed = n);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(
								new Xt(e, this.accumulator, this.seed, this.hasSeed)
							);
						}),
						e
					);
				})(),
				Xt = (function (e) {
					function t(t, n, r, i) {
						var o = e.call(this, t) || this;
						return (
							(o.accumulator = n),
							(o._seed = r),
							(o.hasSeed = i),
							(o.index = 0),
							o
						);
					}
					return (
						i(t, e),
						Object.defineProperty(t.prototype, "seed", {
							get: function () {
								return this._seed;
							},
							set: function (e) {
								(this.hasSeed = !0), (this._seed = e);
							},
							enumerable: !0,
							configurable: !0,
						}),
						(t.prototype._next = function (e) {
							if (this.hasSeed) return this._tryNext(e);
							(this.seed = e), this.destination.next(e);
						}),
						(t.prototype._tryNext = function (e) {
							var t,
								n = this.index++;
							try {
								t = this.accumulator(this.seed, e, n);
							} catch (e) {
								this.destination.error(e);
							}
							(this.seed = t), this.destination.next(t);
						}),
						t
					);
				})(m),
				$t = (function () {
					function e() {
						return (
							Error.call(this),
							(this.message = "argument out of range"),
							(this.name = "ArgumentOutOfRangeError"),
							this
						);
					}
					return (e.prototype = Object.create(Error.prototype)), e;
				})();
			function Zt(e) {
				return function (t) {
					return 0 === e ? wt() : t.lift(new en(e));
				};
			}
			var en = (function () {
					function e(e) {
						if (((this.total = e), this.total < 0)) throw new $t();
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new tn(e, this.total));
						}),
						e
					);
				})(),
				tn = (function (e) {
					function t(t, n) {
						var r = e.call(this, t) || this;
						return (r.total = n), (r.ring = new Array()), (r.count = 0), r;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							var t = this.ring,
								n = this.total,
								r = this.count++;
							t.length < n ? t.push(e) : (t[r % n] = e);
						}),
						(t.prototype._complete = function () {
							var e = this.destination,
								t = this.count;
							if (t > 0)
								for (
									var n = this.count >= this.total ? this.total : this.count,
										r = this.ring,
										i = 0;
									i < n;
									i++
								) {
									var o = t++ % n;
									e.next(r[o]);
								}
							e.complete();
						}),
						t
					);
				})(m);
			function nn(e) {
				return (
					void 0 === e && (e = null),
					function (t) {
						return t.lift(new rn(e));
					}
				);
			}
			var rn = (function () {
					function e(e) {
						this.defaultValue = e;
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new on(e, this.defaultValue));
						}),
						e
					);
				})(),
				on = (function (e) {
					function t(t, n) {
						var r = e.call(this, t) || this;
						return (r.defaultValue = n), (r.isEmpty = !0), r;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							(this.isEmpty = !1), this.destination.next(e);
						}),
						(t.prototype._complete = function () {
							this.isEmpty && this.destination.next(this.defaultValue),
								this.destination.complete();
						}),
						t
					);
				})(m);
			function sn(e, t, n) {
				return 0 === n ? [t] : (e.push(t), e);
			}
			function an() {
				return (function (e, t) {
					return arguments.length >= 2
						? function (n) {
								return P(Yt(e, t), Zt(1), nn(t))(n);
						  }
						: function (t) {
								return P(
									Yt(function (t, n, r) {
										return e(t, n, r + 1);
									}),
									Zt(1)
								)(t);
						  };
				})(sn, []);
			}
			function un(e) {
				return function (t) {
					return 0 === e ? wt() : t.lift(new cn(e));
				};
			}
			var cn = (function () {
					function e(e) {
						if (((this.total = e), this.total < 0)) throw new $t();
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new ln(e, this.total));
						}),
						e
					);
				})(),
				ln = (function (e) {
					function t(t, n) {
						var r = e.call(this, t) || this;
						return (r.total = n), (r.count = 0), r;
					}
					return (
						i(t, e),
						(t.prototype._next = function (e) {
							var t = this.total,
								n = ++this.count;
							n <= t &&
								(this.destination.next(e),
								n === t && (this.destination.complete(), this.unsubscribe()));
						}),
						t
					);
				})(m),
				fn = (function () {
					function e() {
						return (
							Error.call(this),
							(this.message = "Timeout has occurred"),
							(this.name = "TimeoutError"),
							this
						);
					}
					return (e.prototype = Object.create(Error.prototype)), e;
				})();
			function pn(e) {
				return e instanceof Date && !isNaN(+e);
			}
			var hn = (function () {
					function e(e, t, n, r) {
						(this.waitFor = e),
							(this.absoluteTimeout = t),
							(this.withObservable = n),
							(this.scheduler = r);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(
								new gn(
									e,
									this.absoluteTimeout,
									this.waitFor,
									this.withObservable,
									this.scheduler
								)
							);
						}),
						e
					);
				})(),
				gn = (function (e) {
					function t(t, n, r, i, o) {
						var s = e.call(this, t) || this;
						return (
							(s.absoluteTimeout = n),
							(s.waitFor = r),
							(s.withObservable = i),
							(s.scheduler = o),
							s.scheduleTimeout(),
							s
						);
					}
					return (
						i(t, e),
						(t.dispatchTimeout = function (e) {
							var t = e.withObservable;
							e._unsubscribeAndRecycle(), e.add(Y(t, new Q(e)));
						}),
						(t.prototype.scheduleTimeout = function () {
							var e = this.action;
							e
								? (this.action = e.schedule(this, this.waitFor))
								: this.add(
										(this.action = this.scheduler.schedule(
											t.dispatchTimeout,
											this.waitFor,
											this
										))
								  );
						}),
						(t.prototype._next = function (t) {
							this.absoluteTimeout || this.scheduleTimeout(),
								e.prototype._next.call(this, t);
						}),
						(t.prototype._unsubscribe = function () {
							(this.action = void 0),
								(this.scheduler = null),
								(this.withObservable = null);
						}),
						t
					);
				})(J);
			function dn(e, t) {
				return (
					void 0 === t && (t = ne),
					(function (e, t, n) {
						return (
							void 0 === n && (n = ne),
							function (r) {
								var i = pn(e),
									o = i ? +e - n.now() : Math.abs(e);
								return r.lift(new hn(o, i, t, n));
							}
						);
					})(e, Pt(new fn()), t)
				);
			}
			function yn(e) {
				return function (t) {
					var n = new mn(e),
						r = t.lift(n);
					return (n.caught = r);
				};
			}
			var mn = (function () {
					function e(e) {
						this.selector = e;
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new bn(e, this.selector, this.caught));
						}),
						e
					);
				})(),
				bn = (function (e) {
					function t(t, n, r) {
						var i = e.call(this, t) || this;
						return (i.selector = n), (i.caught = r), i;
					}
					return (
						i(t, e),
						(t.prototype.error = function (t) {
							if (!this.isStopped) {
								var n = void 0;
								try {
									n = this.selector(t, this.caught);
								} catch (t) {
									return void e.prototype.error.call(this, t);
								}
								this._unsubscribeAndRecycle();
								var r = new Q(this);
								this.add(r);
								var i = Y(n, r);
								i !== r && this.add(i);
							}
						}),
						t
					);
				})(J);
			var wn = (function () {
					function e(e) {
						this.notifier = e;
					}
					return (
						(e.prototype.call = function (e, t) {
							var n = new Sn(e),
								r = Y(this.notifier, new Q(n));
							return r && !n.seenValue ? (n.add(r), t.subscribe(n)) : n;
						}),
						e
					);
				})(),
				Sn = (function (e) {
					function t(t) {
						var n = e.call(this, t) || this;
						return (n.seenValue = !1), n;
					}
					return (
						i(t, e),
						(t.prototype.notifyNext = function () {
							(this.seenValue = !0), this.complete();
						}),
						(t.prototype.notifyComplete = function () {}),
						t
					);
				})(J);
			var Pn = (function () {
					function e(e, t) {
						(this.delay = e), (this.scheduler = t);
					}
					return (
						(e.prototype.call = function (e, t) {
							return t.subscribe(new vn(e, this.delay, this.scheduler));
						}),
						e
					);
				})(),
				vn = (function (e) {
					function t(t, n, r) {
						var i = e.call(this, t) || this;
						return (
							(i.delay = n),
							(i.scheduler = r),
							(i.queue = []),
							(i.active = !1),
							(i.errored = !1),
							i
						);
					}
					return (
						i(t, e),
						(t.dispatch = function (e) {
							for (
								var t = e.source,
									n = t.queue,
									r = e.scheduler,
									i = e.destination;
								n.length > 0 && n[0].time - r.now() <= 0;

							)
								n.shift().notification.observe(i);
							if (n.length > 0) {
								var o = Math.max(0, n[0].time - r.now());
								this.schedule(e, o);
							} else this.unsubscribe(), (t.active = !1);
						}),
						(t.prototype._schedule = function (e) {
							(this.active = !0),
								this.destination.add(
									e.schedule(t.dispatch, this.delay, {
										source: this,
										destination: this.destination,
										scheduler: e,
									})
								);
						}),
						(t.prototype.scheduleNotification = function (e) {
							if (!0 !== this.errored) {
								var t = this.scheduler,
									n = new An(t.now() + this.delay, e);
								this.queue.push(n), !1 === this.active && this._schedule(t);
							}
						}),
						(t.prototype._next = function (e) {
							this.scheduleNotification(At.createNext(e));
						}),
						(t.prototype._error = function (e) {
							(this.errored = !0),
								(this.queue = []),
								this.destination.error(e),
								this.unsubscribe();
						}),
						(t.prototype._complete = function () {
							this.scheduleNotification(At.createComplete()),
								this.unsubscribe();
						}),
						t
					);
				})(m),
				An = (function () {
					return function (e, t) {
						(this.time = e), (this.notification = t);
					};
				})(),
				On =
					(n(44),
					function (e) {
						var t = "function" == typeof Symbol && Symbol.iterator,
							n = t && e[t],
							r = 0;
						if (n) return n.call(e);
						if (e && "number" == typeof e.length)
							return {
								next: function () {
									return (
										e && r >= e.length && (e = void 0),
										{ value: e && e[r++], done: !e }
									);
								},
							};
						throw new TypeError(
							t ? "Object is not iterable." : "Symbol.iterator is not defined."
						);
					}),
				Tn = function (e, t) {
					var n = "function" == typeof Symbol && e[Symbol.iterator];
					if (!n) return e;
					var r,
						i,
						o = n.call(e),
						s = [];
					try {
						for (; (void 0 === t || t-- > 0) && !(r = o.next()).done; )
							s.push(r.value);
					} catch (e) {
						i = { error: e };
					} finally {
						try {
							r && !r.done && (n = o.return) && n.call(o);
						} finally {
							if (i) throw i.error;
						}
					}
					return s;
				},
				Cn = ot.manager.ArgumentsEvent.EventClass,
				Rn = ot.manager.ArgumentsEvent.Actions,
				En = "true" === window.disable_wt,
				Mn = parseInt(window.freeslots || "3");
			var Ln = function (e, t, n, r) {
					return (
						(e.endTimestamp = new Date()),
						(e.mode = t),
						r && (e.peer = r),
						n && (e.startTimestamp = n),
						e
					);
				},
				xn = function (e, t) {
					if (e.length < t) return [e];
					for (var n = [], r = 0; r < e.byteLength; r += t) {
						var i = e.buffer.slice(r, r + t);
						n.push(new Uint8Array(i));
					}
					return n;
				},
				Dn = function (e, t, n) {
					return G(fetch(e, n)).pipe(
						K(function (e) {
							return G(e.arrayBuffer());
						}),
						j(function (e) {
							return (t.content = new Uint8Array(e)), t;
						})
					);
				},
				In = function () {
					var e = this;
					(this.freeSlots = Mn),
						(this.storage = new Array()),
						(this.resourceAvailability = new Map()),
						(this.blacklistingMap = new Map()),
						(this.resourcePosessionMap = new Map()),
						(this.posessionMapDate = new Map()),
						(this.storageSize = 20),
						(this.enableV2V = !0),
						(this.eventSubject = new E()),
						(this.timeoutV2V = 8e3),
						(this.partSize = 15e3),
						(this.occupiedSlots = 0),
						(this.getResourceCounter = 0),
						(this.waitPeerTimeoutUpper = 1e3),
						(this.waitPeerTimeoutLower = 100),
						(this.cdnDownloader = Dn),
						(this.removeToken = function (e) {
							return -1 !== e.indexOf("?") ? e.split("?")[0] : e;
						}),
						(this.setCDNDownloader = function (t) {
							return (e.cdnDownloader = t), e;
						}),
						(this.setStorageSize = function (t) {
							return (e.storageSize = t), e;
						}),
						(this.setRandomWaitForPeers = function (t) {
							return (
								(e.waitPeerTimeoutLower = t[0]),
								(e.waitPeerTimeoutUpper = t[1]),
								e
							);
						}),
						(this.setAllowByteRequest = function (t) {
							return (e.allowByteRequest = t), e;
						}),
						(this.setPartSize = function (t) {
							return (e.partSize = t), e;
						}),
						(this.setTimeoutV2V = function (t) {
							return (e.timeoutV2V = t), e;
						}),
						(this.setEnableV2V = function (t) {
							return (e.enableV2V = t), e;
						}),
						(this.getV2VTimeout = function () {
							return e.timeoutV2V;
						}),
						(this.subscribeEvents = function () {
							return e.eventSubject;
						}),
						(this.clearStorage = function () {
							return (
								e.storage.splice(0, e.storage.length),
								e.resourcePosessionMap.clear(),
								e.posessionMapDate.clear(),
								e
							);
						}),
						(this.bindSwarmManager = function (t) {
							return (
								(e.swarmManager = t),
								(e.subscriptionSwarmManager = e.swarmManager.subscribe({
									next: e.handleResourceMessage,
								})),
								e.swarmManager
									.subscribeEvents()
									.pipe(
										Gt(function (e) {
											return (
												1025 === e.Type &&
												null !== e.ArgumentsEvent &&
												0 === e.ArgumentsEvent.EventName &&
												1 === e.ArgumentsEvent.Action &&
												null !== e.ArgumentsEvent.RemotePeerID
											);
										})
									)
									.subscribe({
										next: function (t) {
											e.swarmManager.next([
												t.ArgumentsEvent.RemotePeerID,
												e.createPossesionMessage(),
											]);
										},
									}),
								(e.uploadingSuject = new E()),
								e
									.buildSendingPipeline(e.uploadingSuject, e.swarmManager)
									.subscribe(),
								e
							);
						}),
						(this.buildSendingPipeline = function (t, n) {
							return t.pipe(
								Gt(function () {
									return e.freeSlots > 0;
								}),
								j(function (t) {
									return e.freeSlots--, [t[0], t[1], t[2], t[2].length];
								}),
								K(function (t) {
									var r = new Date().getTime(),
										i = t[0],
										o = t[1],
										s = t[2],
										a = t[3];
									return G(s).pipe(
										j(function (e, t) {
											return new Dt.peers.Message({
												Type: Dt.peers.MessageType.MessageTypeSatisfy,
												ArgumentsSatisfy: {
													Content: e,
													PartNumber: t,
													PartTotal: a,
													Resource: o,
												},
											});
										}),
										K(function (t) {
											return n.next([i, t]).pipe(
												j(function (n) {
													var o, s;
													return (
														t.ArgumentsSatisfy.PartNumber ===
															t.ArgumentsSatisfy.PartTotal - 1 &&
															(e.freeSlots++,
															e.p2pStatsStore.addUpload(
																(null ===
																	(s =
																		null === (o = t.ArgumentsSatisfy) ||
																		void 0 === o
																			? void 0
																			: o.Content) || void 0 === s
																	? void 0
																	: s.byteLength) || 0
															),
															e.eventSubject.next(
																new ot.manager.Message({
																	Type: 1025,
																	ArgumentsEvent: {
																		EventName: Cn.RESOURCE,
																		Action: Rn.UPLOADED,
																		RemotePeerID: i,
																		ArgumentsResourceUploaded: {
																			URL: t.ArgumentsSatisfy.Resource,
																			TimeSpentMs: Date.now() - r,
																			SizeBytes:
																				t.ArgumentsSatisfy.PartNumber *
																					e.partSize +
																				t.ArgumentsSatisfy.Content.byteLength,
																			Ts: Date.now(),
																			Mode: "v2v",
																			Upload: !0,
																		},
																	},
																})
															)),
														n
													);
												})
											);
										})
									);
								})
							);
						}),
						(this.getResourceInStorage = function (t) {
							var n, r;
							try {
								for (
									var i = On(e.storage), o = i.next();
									!o.done;
									o = i.next()
								) {
									var s = o.value;
									if (s[0] === t) return s[1];
								}
							} catch (e) {
								n = { error: e };
							} finally {
								try {
									o && !o.done && (r = i.return) && r.call(i);
								} finally {
									if (n) throw n.error;
								}
							}
							return null;
						}),
						(this.addResourceToStorage = function (t, n) {
							e.storage.some(function (e) {
								return e[0] === t;
							}) ||
								(e.storage.length >= e.storageSize && e.storage.shift(),
								e.storage.push([t, new Uint8Array(n)]));
						}),
						(this.getAvailablePeersFor = function (t) {
							var n = e.useWaitingTimeControl();
							return me(St(0), ce(100)).pipe(
								K(function (r) {
									return G(e.resourcePosessionMap).pipe(
										Gt(function (t) {
											var r;
											return e.swarmManager.hasPeer(t[0])
												? !(
														n &&
														e.blacklistingMap.has(t[0]) &&
														(null === (r = e.blacklistingMap.get(t[0])) ||
														void 0 === r
															? void 0
															: r.getTime()) /
															1e3 +
															60 >
															new Date().getTime() / 1e3
												  )
												: (e.purgePeer(t[0]), !1);
										}),
										Gt(function (n) {
											return (
												(function (e, t) {
													return -1 !== t.indexOf(_t(e));
												})(t, n[1]) && e.enableV2V
											);
										}),
										j(function (e) {
											return e[0];
										}),
										an(),
										j(function (n) {
											var r = Array.from(n);
											return (
												0 !== r.length &&
													e.eventSubject.next(
														new ot.manager.Message({
															Type: ot.manager.MessageType.MessageTypeEvent,
															Timestamp: Date.now(),
															ArgumentsEvent: {
																EventName: Cn.RESOURCE,
																Action: Rn.AVAILABILITY,
																ArgumentsResourceAvailability: {
																	Pids: r,
																	URL: t,
																},
															},
														})
													),
												n
											);
										})
									);
								})
							);
						}),
						(this.purgePeer = function (t) {
							e.resourceAvailability.forEach(function (e) {
								e.delete(t);
							}),
								e.blacklistingMap.delete(t),
								e.resourcePosessionMap.delete(t),
								e.posessionMapDate.delete(t);
						}),
						(this.getResource = function (t, n) {
							var r = 0;
							e.enableV2V = e.p2pStatsStore.safeToUseV2V(!1, 4);
							var i = e.useWaitingTimeControl(),
								o = i ? e.getV2VTimeout() : e.timeoutV2V;
							if (i) {
								if (e.enableV2V) {
									var s = Tn(e.p2pStatsStore.getActionWaitingTime(), 2),
										a = s[0],
										u = s[1];
									r = Math.round(Math.random() * (a - u) + u);
								}
							} else if (e.enableV2V) {
								var c = Tn(e.p2pStatsStore.getActionWaitingTime(!0), 2);
								(a = c[0]),
									(u = c[1]),
									(r = Math.round(Math.random() * (a - u) + u));
							}
							0 == r && (e.enableV2V = !1), e.getResourceCounter++;
							var l = e.removeToken(t),
								f = { url: l, startTimestamp: new Date() };
							return e
								.getAvailablePeersFor(l)
								.pipe(
									Gt(function (e) {
										return 0 !== e.length;
									}),
									un(1),
									j(function (e) {
										return [e, f];
									}),
									dn(r),
									K(function (t) {
										var n = t[0].map(function (t) {
											return [
												t,
												e.posessionMapDate.has(t)
													? e.posessionMapDate.get(t).getTime()
													: 0,
											];
										});
										return e
											.p2pDownload(
												l,
												n.map(function (e) {
													return e[0];
												}),
												t[1]
											)
											.pipe(
												j(function (e) {
													return Ln(f, "v2v");
												}),
												j(function (e) {
													return e;
												})
											);
									}),
									yn(function (n) {
										var r = new Date();
										return (
											Object(ht.c)(
												"resource-manager",
												"no peer available after " +
													(r.getTime() - f.startTimestamp.getTime())
											),
											e.cdnDownloader(t, f).pipe(
												j(function (e) {
													return Ln(f, "cdn", r);
												})
											)
										);
									}),
									dn(o),
									yn(function (n) {
										var r = new Date();
										return (
											f.content && f.content.byteLength,
											Object(ht.c)(
												"resource-manager",
												"v2v timeout: " +
													JSON.stringify(f) +
													" / " +
													new Date() +
													". Transfered " +
													f.transfered +
													" / " +
													f.total
											),
											e.swarmManager.getID(),
											e.getV2VTimeout(),
											f.transfered,
											f.total,
											e.blacklistingMap.set(f.peer, new Date()),
											e.cdnDownloader(t, f).pipe(
												j(function (e) {
													return Ln(f, "cdn", r);
												})
											)
										);
									})
								)
								.pipe(
									j(function (t) {
										return (
											e.eventSubject.next(
												new ot.manager.Message({
													Type: 1025,
													ArgumentsEvent: {
														EventName:
															ot.manager.ArgumentsEvent.EventClass.RESOURCE,
														Action:
															ot.manager.ArgumentsEvent.Actions.DOWNLOADED,
														RemotePeerID: t.peer || "",
														ArgumentsResourceDownloaded: {
															Mode: t.mode,
															URL: t.url,
															Ts: Date.now(),
															TimeSpentMs:
																t.endTimestamp.getTime() -
																t.startTimestamp.getTime(),
															SizeBytes: t.content.byteLength,
															Upload: !1,
														},
													},
												})
											),
											t.content
										);
									})
								)
								.toPromise()
								.then(function (t) {
									return (
										e.addResourceToStorage(l, t),
										e.swarmManager
											.broadcastMessage(e.createPossesionMessage())
											.subscribe(function () {}),
										t
									);
								});
						}),
						(this.handleResourceMessage = function (t) {
							var n = t[0],
								r = t[1].ArgumentsResource;
							if (
								t[1].Type === Dt.peers.MessageType.MessageTypePossession ||
								t[1].Type === Dt.peers.MessageType.MessageTypeAck ||
								(r && r.URL && "" !== r.URL)
							)
								if (n && "" !== n)
									switch (t[1].Type) {
										case Dt.peers.MessageType.MessageTypePossession:
											if (
												t[1].ArgumentsPossession &&
												t[1].ArgumentsPossession.URLHashSet
											) {
												var i = t[1].ArgumentsPossession.URLHashSet;
												e.resourcePosessionMap.set(
													t[0],
													(function (e) {
														if (e.length % 2 != 0)
															throw new Error(
																"cannot assemble a uint8array which hasn't even number of elements"
															);
														for (
															var t = new Uint16Array(e.length / 2), n = 0;
															n < t.length;
															++n
														)
															t[n] = e[2 * n] + (e[2 * n + 1] << 8);
														return t;
													})(i)
												),
													e.posessionMapDate.set(t[0], new Date());
											}
											break;
										case Dt.peers.MessageType.MessageTypeRequest:
											if (null == r ? void 0 : r.URL) {
												var o = e.getResourceInStorage(r.URL);
												o &&
													(e.swarmManager.addResourceActions(n, "request"),
													e.uploadingSuject.next([
														n,
														r.URL,
														xn(o, e.partSize),
													]));
											}
											break;
										case Dt.peers.MessageType.MessageTypeAck:
											e.p2pStatsStore.addSuccessUpload();
									}
								else
									console.error(
										"resource-manager",
										"peerID is not valid: " + n
									);
						}),
						(this.useWaitingTimeControl = function () {
							return !En && 0 === e.swarmManager.getBucketID();
						}),
						(this.createPossesionMessage = function () {
							var t;
							return new Dt.peers.Message({
								Type: Dt.peers.MessageType.MessageTypePossession,
								ArgumentsPossession: {
									URLHashSet: new Uint8Array(
										((t = e.storage
											.map(function (e) {
												return e[0];
											})
											.sort()),
										new Uint16Array(
											t.map(function (e) {
												return _t(e);
											})
										)).buffer
									),
								},
							});
						}),
						(this.p2pDownload = function (t, n, r) {
							return (
								new Date(),
								G(n).pipe(
									un(1),
									K(function (n) {
										return (
											(r.peer = n),
											e.swarmManager
												.next([
													n,
													new Dt.peers.Message({
														Type: Dt.peers.MessageType.MessageTypeRequest,
														ArgumentsResource: { URL: t },
													}),
												])
												.pipe(
													j(function (e) {
														return [n, e];
													})
												)
										);
									}),
									j(function (e) {
										return e[0];
									}),
									K(function (n) {
										var i,
											o = new Set(),
											s = new E();
										return e.swarmManager.getPeerChannels().pipe(
											Gt(function (e) {
												return e[0] === n;
											}),
											Gt(function (e) {
												return (
													e[1].Type === Dt.peers.MessageType.MessageTypeSatisfy
												);
											}),
											Gt(function (e) {
												return (
													e[1].ArgumentsSatisfy &&
													e[1].ArgumentsSatisfy.Resource === t
												);
											}),
											j(function (e) {
												var t, n, i, a;
												return (
													o.add(e[1].ArgumentsSatisfy.PartNumber),
													(r.transfered =
														null !==
															(n =
																null === (t = e[1].ArgumentsSatisfy) ||
																void 0 === t
																	? void 0
																	: t.PartNumber) && void 0 !== n
															? n
															: void 0),
													(r.total =
														null !==
															(a =
																null === (i = e[1].ArgumentsSatisfy) ||
																void 0 === i
																	? void 0
																	: i.PartTotal) && void 0 !== a
															? a
															: void 0),
													o.size === e[1].ArgumentsSatisfy.PartTotal &&
														s.next(),
													e[1].ArgumentsSatisfy.Content
												);
											}),
											((i = s.pipe(
												(function (e, t) {
													void 0 === t && (t = ne);
													var n = pn(e) ? +e - t.now() : Math.abs(e);
													return function (e) {
														return e.lift(new Pn(n, t));
													};
												})(10)
											)),
											function (e) {
												return e.lift(new wn(i));
											}),
											an(),
											j(function (e) {
												var t, n, i, o;
												return (
													(r.content =
														((n = (t = e).reduce(function (e, t) {
															return e + t.byteLength;
														}, 0)),
														(i = new Uint8Array(n)),
														(o = 0),
														t.forEach(function (e) {
															i.set(e, o), (o += e.byteLength);
														}),
														i)),
													r
												);
											})
										);
									})
								)
							);
						});
				},
				kn =
					(ot.manager.ArgumentsEvent.EventClass,
					ot.manager.ArgumentsEvent.Actions,
					function () {
						var e = this;
						(this.eventSubject = new E()),
							(this.mapOutputPlugin = new Map()),
							(this.register = function (t) {
								return (
									t.subscribeEvents().subscribe({
										next: function (t) {
											e.eventSubject.next(t);
										},
									}),
									e
								);
							}),
							(this.close = function () {
								e.mapOutputPlugin.forEach(function (e, t) {
									e[1].stop(), e[0].unsubscribe();
								});
							}),
							(this.registerOutput = function (t, n) {
								return e.mapOutputPlugin.has(n)
									? (console.warn("Duplicated op: ", n), e)
									: (e.mapOutputPlugin.set(n, [
											e.eventSubject
												.pipe(
													Gt(function (e) {
														return void 0 !== e.Type;
													}),
													Gt(function (e) {
														return (
															e.Type === ot.manager.MessageType.MessageTypeEvent
														);
													}),
													j(function (e) {
														var t = ot.manager.Message.verify(e);
														return (
															"null" !== t &&
																null !== t &&
																(Object(ht.c)("stats-collector", e),
																Object(ht.b)("stats-collector", t)),
															e
														);
													})
												)
												.subscribe({ next: t.next }),
											t,
									  ]),
									  e);
							}),
							(this.unregisterOutput = function (t) {
								e.mapOutputPlugin.has(t) &&
									e.mapOutputPlugin.get(t)[0].unsubscribe();
							});
					});
			function jn() {
				return de(1);
			}
			function Bn() {
				for (var e = [], t = 0; t < arguments.length; t++) e[t] = arguments[t];
				return jn()(St.apply(void 0, e));
			}
			var Nn,
				Un,
				_n = (function (e) {
					function t() {
						var t = (null !== e && e.apply(this, arguments)) || this;
						return (t.value = null), (t.hasNext = !1), (t.hasCompleted = !1), t;
					}
					return (
						i(t, e),
						(t.prototype._subscribe = function (t) {
							return this.hasError
								? (t.error(this.thrownError), g.EMPTY)
								: this.hasCompleted && this.hasNext
								? (t.next(this.value), t.complete(), g.EMPTY)
								: e.prototype._subscribe.call(this, t);
						}),
						(t.prototype.next = function (e) {
							this.hasCompleted || ((this.value = e), (this.hasNext = !0));
						}),
						(t.prototype.error = function (t) {
							this.hasCompleted || e.prototype.error.call(this, t);
						}),
						(t.prototype.complete = function () {
							(this.hasCompleted = !0),
								this.hasNext && e.prototype.next.call(this, this.value),
								e.prototype.complete.call(this);
						}),
						t
					);
				})(E),
				qn = n(8),
				Vn = n(16),
				Fn = function (e, t) {
					var n = "function" == typeof Symbol && e[Symbol.iterator];
					if (!n) return e;
					var r,
						i,
						o = n.call(e),
						s = [];
					try {
						for (; (void 0 === t || t-- > 0) && !(r = o.next()).done; )
							s.push(r.value);
					} catch (e) {
						i = { error: e };
					} finally {
						try {
							r && !r.done && (n = o.return) && n.call(o);
						} finally {
							if (i) throw i.error;
						}
					}
					return s;
				};
			!(function (e) {
				(e[(e.NoError = 0)] = "NoError"), (e[(e.SendError = 1)] = "SendError");
			})(Nn || (Nn = {})),
				(function (e) {
					(e[(e.CandidateTypeHost = 0)] = "CandidateTypeHost"),
						(e[(e.CandidateTypeServerReflexive = 1)] =
							"CandidateTypeServerReflexive"),
						(e[(e.CandidateTypePeerReflexive = 2)] =
							"CandidateTypePeerReflexive"),
						(e[(e.CandidateTypeRelay = 3)] = "CandidateTypeRelay");
				})(Un || (Un = {}));
			var zn,
				Wn = [{ urls: ["stun:stun.easybroadcast.fr:3478"] }],
				Hn = function (e) {
					var t,
						n = e.candidate.indexOf("candidate:") + 10,
						r = Fn(e.candidate.trim().substr(n).split(/\s+/)).slice(0),
						i = r[4],
						o = r[7];
					if ("" === i) return null;
					switch (o) {
						case "host":
							t = Un.CandidateTypeHost;
							break;
						case "srflx":
							t = Un.CandidateTypeServerReflexive;
							break;
						case "prflx":
							t = Un.CandidateTypePeerReflexive;
							break;
						case "relay":
							t = Un.CandidateTypeRelay;
							break;
						default:
							return null;
					}
					return new ot.manager.IceCandidate({ Type: t, Address: i });
				},
				Gn = (function () {
					function e(e) {
						var t = this;
						(this.timestamp = new Date()),
							(this.iceGatherTimeout = 2e3),
							(this.ID = function () {
								return t.id;
							}),
							(this.next = function (e) {
								return new qn.Observable(function (n) {
									var r = Dt.peers.Message.verify(e);
									null != r && n.error(r);
									try {
										t.syncChannel.send(Dt.peers.Message.encode(e).finish()),
											n.next({ Type: Nn.NoError });
									} catch (e) {
										n.error({ Type: Nn.SendError, Args: e });
									}
									n.complete();
								});
							}),
							(this.onIceCandidateHandle = function (e) {
								"object" == typeof e &&
									void 0 !== e.candidate &&
									null !== e.candidate &&
									t.iceCandidateArray.push(e.candidate);
							}),
							(this.onIceConnectionStateChangeHandle = function (e) {
								switch (e.target.iceConnectionState) {
									case "new":
									case "checking":
										(t.pcCurrentState = "new"),
											t.peerStateChangesSubject.next("new");
										break;
									case "disconnected":
									case "failed":
									case "closed":
										(t.pcCurrentState = "disconnected"),
											t.peerStateChangesSubject.next("disconnected");
								}
							}),
							(this.onIceGatheringStateChangeHandle = function (e) {
								switch (e.target.iceGatheringState) {
									case "gathering":
										t.iceGatherTimer = setTimeout(function () {
											if (t.iceCandidateArray.length)
												return (
													t.iceGatherSubject.next(
														t.parseIceCandidate(t.iceCandidateArray)
													),
													void t.iceGatherSubject.complete()
												);
											console.warn(
												"peer " + t.id + " gather ice candidate timeout"
											),
												t.iceGatherSubject.complete(),
												t.iceGatherTimer &&
													(clearTimeout(t.iceGatherTimer),
													(t.iceGatherTimer = null));
										}, t.iceGatherTimeout);
										break;
									case "complete":
										t.iceCandidateArray.length > 0 &&
											(t.iceGatherSubject.next(
												t.parseIceCandidate(t.iceCandidateArray)
											),
											t.iceGatherSubject.complete()),
											t.iceGatherTimer &&
												(clearTimeout(t.iceGatherTimer),
												(t.iceGatherTimer = null));
								}
							}),
							(this.bindDataChannelHandler = function (e) {
								(e.binaryType = "arraybuffer"),
									(e.onmessage = t.handleIncomingMessage),
									(e.onopen = function () {
										return t.handleDataChannelChange("open");
									}),
									(e.onclose = function () {
										return t.handleDataChannelChange("closed");
									});
							}),
							(this.onDataChannel = function (e) {
								e.channel &&
									((t.syncChannel = e.channel),
									t.bindDataChannelHandler(t.syncChannel));
							}),
							(this.handleIncomingMessage = function (e) {
								if (e.data) {
									var n = void 0;
									try {
										n = Dt.peers.Message.decode(new Uint8Array(e.data));
									} catch (e) {
										return void console.warn(
											"Invalid incoming message from " + t.id + ": " + e
										);
									}
									t.peerChannelSubject.next(n);
								} else console.warn("peer " + t.id + " coming msg has no data");
							}),
							(this.handleDataChannelChange = function (e) {
								switch (e) {
									case "open":
										(t.pcCurrentState = "connected"),
											t.peerStateChangesSubject.next("connected");
										break;
									case "closed":
										(t.pcCurrentState = "disconnected"),
											t.peerStateChangesSubject.next("disconnected");
								}
							}),
							(this.toIceCandidate = function (e) {
								return e.map(function (e) {
									return new RTCIceCandidate({
										candidate: e,
										sdpMLineIndex: 0,
									});
								});
							}),
							(this.parseIceCandidate = function (e) {
								return e
									.filter(function (e) {
										return null !== e;
									})
									.map(function (e) {
										return e.candidate;
									});
							}),
							(this.toSessionSDP = function (e, t) {
								return new RTCSessionDescription({ sdp: e, type: t });
							}),
							(this.parseSDP = function (e) {
								return e.sdp;
							}),
							(this.id = e || null);
						var n = { iceServers: Wn, iceTransportPolicy: "all" };
						(this.peerConnection = new RTCPeerConnection(n)),
							this.peerConnection.addEventListener(
								"icecandidate",
								function (e) {
									return t.onIceCandidateHandle(e);
								}
							),
							this.peerConnection.addEventListener(
								"iceconnectionstatechange",
								function (e) {
									return t.onIceConnectionStateChangeHandle(e);
								}
							),
							this.peerConnection.addEventListener(
								"icegatheringstatechange",
								function (e) {
									return t.onIceGatheringStateChangeHandle(e);
								}
							),
							this.peerConnection.addEventListener("datachannel", function (e) {
								return t.onDataChannel(e);
							}),
							(this.pcCurrentState = "new"),
							(this.peerChannelSubject = new Vn.Subject()),
							(this.iceGatherSubject = new _n()),
							(this.peerStateChangesSubject = new Vn.Subject()),
							(this.iceCandidateArray = new Array());
					}
					return (
						(e.prototype.close = function () {
							try {
								this.syncChannel &&
									(this.syncChannel.close(), (this.syncChannel = null)),
									this.peerConnection &&
										(this.peerConnection.close(), (this.peerConnection = null));
							} catch (e) {}
						}),
						(e.prototype.getAge = function () {
							return new Date().getTime() - this.timestamp.getTime();
						}),
						(e.prototype.sendOffer = function () {
							var e = this,
								t = new qn.Observable(function (t) {
									e.peerConnection
										.createOffer()
										.then(function (n) {
											e.peerConnection
												.setLocalDescription(n)
												.then(function () {
													e.iceGatherSubject.subscribe({
														next: function () {},
														complete: function () {
															if (
																!e.peerConnection ||
																!e.peerConnection.localDescription
															)
																return (
																	console.warn(
																		"peer " +
																			e.id +
																			": localDescription not set yet"
																	),
																	void t.error(
																		new Error("localDescription is null")
																	)
																);
															t.next([
																e.parseSDP(e.peerConnection.localDescription),
																e.parseIceCandidate(e.iceCandidateArray),
															]);
														},
														error: function () {},
													});
												})
												.catch(function (e) {
													t.error(e);
												});
										})
										.catch(function (e) {
											t.error(e);
										});
								});
							return (
								(this.syncChannel =
									this.peerConnection.createDataChannel("sync")),
								this.bindDataChannelHandler(this.syncChannel),
								t
							);
						}),
						(e.prototype.sendAnswer = function (e, t) {
							var n = this;
							return new qn.Observable(function (r) {
								n.peerConnection
									.setRemoteDescription(n.toSessionSDP(e, "offer"))
									.then(function () {
										return n.peerConnection.createAnswer();
									})
									.then(function (e) {
										n.peerConnection
											.setLocalDescription(e)
											.then(function () {
												n.toIceCandidate(t).forEach(function (e, t) {
													return n.peerConnection
														.addIceCandidate(e)
														.catch(function (e) {});
												}),
													n.iceGatherSubject.subscribe({
														next: function () {},
														complete: function () {
															if (
																!n.peerConnection ||
																!n.peerConnection.localDescription
															)
																return (
																	console.warn(
																		"peer " +
																			n.id +
																			": localDescription not set yet"
																	),
																	void r.error(
																		new Error("localDescription is null")
																	)
																);
															n.peerConnection &&
																r.next([
																	n.parseSDP(n.peerConnection.localDescription),
																	n.parseIceCandidate(n.iceCandidateArray),
																]);
														},
														error: function () {},
													});
											})
											.catch(function (e) {
												console.error(
													"peer " +
														n.id +
														" set local description fail, error is: " +
														e.message
												),
													r.error(e);
											});
									})
									.catch(function (e) {
										console.error(
											"peer " +
												n.id +
												" set remote description fail, error is: " +
												e.message
										),
											r.error(e);
									});
							});
						}),
						(e.prototype.receiveAnswer = function (e, t) {
							var n = this;
							return new qn.Observable(function (r) {
								n.peerConnection
									.setRemoteDescription(n.toSessionSDP(e, "answer"))
									.then(function () {
										n.toIceCandidate(t).forEach(function (e, t) {
											n.peerConnection
												.addIceCandidate(e)
												.catch(function (e) {});
										}),
											r.next(!0);
									})
									.catch(function (e) {
										r.next(!1),
											console.error(
												"peer " +
													n.id +
													" set remote description error: " +
													e.message
											);
									});
							});
						}),
						(e.prototype.notifyStateChanges = function (e) {
							return this.peerStateChangesSubject.subscribe(e);
						}),
						(e.prototype.subscribe = function (e) {
							return this.peerChannelSubject.subscribe(e);
						}),
						(e.prototype.getState = function () {
							return this.pcCurrentState;
						}),
						e
					);
				})(),
				Qn = ot.manager.ArgumentsEvent.Actions,
				Jn = ot.manager.ArgumentsEvent.EventClass,
				Yn = ot.manager.SwarmChangeReason,
				Kn = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
				Xn = {
					createPeerConnector: function (e) {
						return new Gn(e || null);
					},
					gatherIceCandidates: function () {
						return new qn.Observable(function (e) {
							var t = new RTCPeerConnection({
									iceServers: Wn,
									iceTransportPolicy: "all",
								}),
								n = new Array(),
								r = null;
							(t.onicecandidate = function (t) {
								"object" == typeof t &&
									void 0 !== t.candidate &&
									(null === t.candidate &&
										(e.next(
											n
												.filter(function (e) {
													return null !== e;
												})
												.map(function (e) {
													return Hn(e);
												})
												.filter(function (e, t, n) {
													return (
														n.findIndex(function (t) {
															return (
																t &&
																t.Type === e.Type &&
																t.Address === e.Address
															);
														}) === t
													);
												})
										),
										e.complete(),
										r && (clearTimeout(r), (r = null))),
									n.push(t.candidate));
							}),
								(t.onicegatheringstatechange = function (e) {
									null != t &&
										"complete" === t.iceGatheringState &&
										(t.close(), (t = null));
								}),
								setTimeout(function () {
									null != t && (t.close(), (t = null)),
										n.length &&
											(e.next(
												n
													.filter(function (e) {
														return null !== e;
													})
													.map(function (e) {
														return Hn(e);
													})
													.filter(function (e, t, n) {
														return e;
													})
													.filter(function (e, t, n) {
														return (
															n.findIndex(function (t) {
																return (
																	t &&
																	t.Type === e.Type &&
																	t.Address === e.Address
																);
															}) === t
														);
													})
											),
											e.complete()),
										r && (clearTimeout(r), (r = null)),
										n.length ||
											e.error(
												new Error("Timeout while gathering ICE candidates")
											);
								}, 3e3),
								t.createDataChannel(""),
								t
									.createOffer({ offerToReceiveAudio: !0 })
									.then(function (e) {
										return t.setLocalDescription(e);
									})
									.catch(function (t) {
										e.error(t);
									});
						});
					},
				};
			!(function (e) {
				(e[(e.PeerNoneExisting = 0)] = "PeerNoneExisting"),
					(e[(e.PeerBroke = 1)] = "PeerBroke"),
					(e[(e.NoError = 2)] = "NoError"),
					(e[(e.Timeout = 3)] = "Timeout");
			})(zn || (zn = {}));
			var $n = (function () {
				function e(e) {
					var t = this;
					(this.test_string = "Library Luyi ABtest 110s in production"),
						(this.iceTimeout = 8e3),
						(this.swarmSize = 0),
						(this.maxSwarmSize = 10),
						(this.sendMessageTimeout = 4e3),
						(this.connectionTimeout = 25e3),
						(this.pingPongCheckInterval = 1e4),
						(this.pingPongInterval = 5e3),
						(this.pingPongMaxAllowedDrift = 10),
						(this.offerMaxPercentage = 0.5),
						(this.iceCandidateCacheTTL = 1e5),
						(this.setPeerConnectorUtils = function (e) {
							t.peerConnectorUtil = e;
						}),
						(this.start = function (e) {
							t.populatingSubscription &&
								t.populatingSubscription.unsubscribe(),
								t.setSleep(1e4).then(function () {
									t.populatingSubscription = me(
										ce(e).pipe(
											(function () {
												for (var e = [], t = 0; t < arguments.length; t++)
													e[t] = arguments[t];
												var n = e[e.length - 1];
												return ge(n)
													? (e.pop(),
													  function (t) {
															return Bn(e, t, n);
													  })
													: function (t) {
															return Bn(e, t);
													  };
											})(0)
										)
									)
										.pipe(
											Gt(function () {
												return t.getSwarmSize().All < t.maxSwarmSize;
											})
										)
										.subscribe({
											next: function () {
												var e = t.getSwarmSize();
												t.managerConnector.next(
													new ot.manager.Message({
														Type: ot.manager.MessageType.MessageTypeGiveMePeers,
														ArgumentsGiveMePeers: {
															Current: e.All,
															CDNThroughput:
																t.managerConnector.p2pStatsStore.getCDNThroughput(),
															Want:
																t.maxSwarmSize * t.offerMaxPercentage - e.Offer,
															Accept:
																t.maxSwarmSize * (1 - t.offerMaxPercentage) -
																e.Answer,
															CurrentTime: t.currentTimeVOD,
														},
													})
												);
											},
										});
								});
						}),
						(this.close = function () {
							t.populatingSubscription &&
								t.populatingSubscription.unsubscribe(),
								t.peerManagerSubscription &&
									t.peerManagerSubscription.unsubscribe(),
								t.managerStateSubscription &&
									t.managerStateSubscription.unsubscribe(),
								t.peerList.forEach(function (e) {
									e.close();
								});
						}),
						(this.ID = function () {
							return t.id;
						}),
						(this.getPeerChannels = function () {
							return t.peerMessageSubject;
						}),
						(this.setPingPongCheckInterval = function (e) {
							return (t.pingPongCheckInterval = e), t;
						}),
						(this.setMaxSwarmSize = function (e) {
							return (t.maxSwarmSize = e), t;
						}),
						(this.setPingPongInterval = function (e) {
							return (t.pingPongInterval = e), t;
						}),
						(this.setMaxOfferPercentage = function (e) {
							return (t.offerMaxPercentage = e), t;
						}),
						(this.setMaxAllowedPingPongDrift = function (e) {
							return (t.pingPongMaxAllowedDrift = e), t;
						}),
						(this.setSendMessageTimeout = function (e) {
							return (t.sendMessageTimeout = e), t;
						}),
						(this.usePeerConnectorUtil = function (e) {
							return (t.peerConnectorUtil = e), t;
						}),
						(this.hasPeer = function (e) {
							return t.peerList.has(e);
						}),
						(this.isAnswerSwarmFull = function () {
							return (
								t.getSwarmSize().Answer >=
								t.maxSwarmSize * (1 - t.offerMaxPercentage)
							);
						}),
						(this.select = function (e) {
							return G(t.peerList).pipe(
								Gt(function (t) {
									return e(t[1]);
								})
							);
						}),
						(this.subscribeEvents = function () {
							return t.eventSubject;
						}),
						(this.getPeerList = function () {
							return t.peerList;
						}),
						(this.getPeerInfo = function () {
							return t.peerAdditionalInfo;
						}),
						(this.bind = function (e) {
							return (
								(t.managerConnector = e),
								(t.peerManagerSubscription = t.managerConnector.subscribe({
									next: t.handleIncomingMessage,
								})),
								(t.managerStateSubscription =
									t.managerConnector.notifyStateChanges({
										next: function (e) {
											"con" === e &&
												t.registerParm &&
												t.register(
													t.registerParm.Bandwidth,
													t.registerParm.Codec,
													t.registerParm.Url
												);
										},
									})),
								t
							);
						}),
						(this.register = function (e, n, r, i) {
							return (
								i && t.empty(),
								(t.registerParm = new ot.manager.ArgumentsRegister({
									Bandwidth: e,
									Codec: n,
									Url: r,
								})),
								t.lastGatherCalled &&
								Date.now() - t.lastGatherCalled < t.iceCandidateCacheTTL &&
								t.iceCandidateCache
									? ((t.registerParm.Candidates = t.iceCandidateCache),
									  t.managerConnector.next(
											new ot.manager.Message({
												Type: ot.manager.MessageType.MessageTypeRegister,
												ArgumentsRegister: t.registerParm,
											})
									  ),
									  St(!0).toPromise())
									: new A(function (e) {
											t.peerConnectorUtil.gatherIceCandidates().subscribe({
												next: function (n) {
													(t.iceCandidateCache = n),
														(t.lastGatherCalled = Date.now()),
														(t.registerParm.Candidates = n),
														t.managerConnector.next(
															new ot.manager.Message({
																Type: ot.manager.MessageType
																	.MessageTypeRegister,
																ArgumentsRegister: t.registerParm,
															})
														),
														e.next(!0);
												},
												complete: function () {
													return e.complete;
												},
												error: function (t) {
													e.next(!1), Object(ht.b)(t);
												},
											});
									  }).toPromise()
							);
						}),
						(this.multicastMessage = function (e, n) {
							return n.pipe(
								Gt(function (e) {
									return (
										"connected" === t.peerAdditionalInfo.get(e[0]).PeerState
									);
								}),
								K(function (n) {
									return t.next([n[0], e]);
								})
							);
						}),
						(this.broadcastMessage = function (e) {
							return t.multicastMessage(e, G(t.peerList));
						}),
						(this.subscribe = function (e) {
							return t.peerMessageSubject
								.pipe(
									j(function (e) {
										return e;
									})
								)
								.subscribe(e);
						}),
						(this.next = function (e) {
							var n = t.peerList.get(e[0]),
								r = Date.now();
							return n
								? n.next(e[1]).pipe(
										K(function (e) {
											return e.Type === Nn.NoError
												? St({ Type: zn.NoError })
												: St({ Type: zn.PeerBroke });
										}),
										dn(t.sendMessageTimeout),
										yn(function () {
											return St({ Type: zn.Timeout });
										}),
										j(function (n) {
											var i = 6;
											switch (e[1].Type) {
												case Dt.peers.MessageType.MessageTypePossession:
													i = 2;
													break;
												case Dt.peers.MessageType.MessageTypeRequest:
													i = 3;
													break;
												case Dt.peers.MessageType.MessageTypeSatisfy:
													i = 4;
													break;
												case Dt.peers.MessageType.MessageTypeAck:
													i = 5;
													break;
												default:
													return (
														console.error(
															"swarm-manager",
															"Peer MessageType not handled by stats..",
															e[1].Type
														),
														n
													);
											}
											return (
												(t.peerAdditionalInfo.get(e[0]).SendSeq[i] += 1),
												(t.peerAdditionalInfo.get(e[0]).SendTime[i] +=
													Date.now() - r),
												n
											);
										})
								  )
								: G([{ Type: zn.PeerNoneExisting }]).pipe(
										j(function (e) {
											return Pt(e);
										}),
										jn()
								  );
						}),
						(this.empty = function () {
							Array.from(t.peerList.keys()).forEach(function (e) {
								t.cleanPeerConnector(t.peerList.get(e), Yn.CHANNELSWITCH);
							});
						}),
						(this.getID = function () {
							return t.managerConnector.getID();
						}),
						(this.getBucketID = function () {
							return t.managerConnector.getBucketID();
						}),
						(this.cleanPeerConnector = function (e, n) {
							if ((e.close(), t.peerAdditionalInfo.has(e.ID()))) {
								Object(ht.c)(
									"swarm-manager",
									"clear peerConnector: " + e.ID() + " / rs: " + n
								);
								var r = t.peerAdditionalInfo.get(e.ID());
								r.Subscriptions.forEach(function (e) {
									e && e.unsubscribe();
								}),
									r.PingPongRegi.forEach(function (r, i) {
										t.eventSubject.next(
											new ot.manager.Message({
												Type: 1025,
												ArgumentsEvent: {
													EventName: Jn.PINGPONG,
													Action: Qn.EXCHANGE,
													ArgumentsPingPongExchange: {
														Seq: i,
														Pid: e.ID(),
														Start: r,
														End: Date.now(),
														State: n.toString(),
													},
												},
											})
										);
									});
							}
							t.clearConnectionTimeoutFor(e.ID()),
								t.peerList.delete(e.ID()),
								t.peerAdditionalInfo.delete(e.ID()),
								(e = null),
								t.eventSubject.next(
									new ot.manager.Message({
										Type: 1025,
										ArgumentsEvent: {
											EventName: Jn.SWARM,
											Action: Qn.SIZEUPDATE,
											ArgumentsSwarmSizeUpdate: {
												Size: t.peerList.size,
												Reason: n,
											},
										},
									})
								);
						}),
						(this.getSwarmSize = function () {
							var e = { All: 0, Offer: 0, Answer: 0 };
							return (
								t.peerAdditionalInfo.forEach(function (t, n) {
									e.All++,
										"a" === t.PeerType && e.Offer++,
										"b" === t.PeerType && e.Answer++;
								}),
								e
							);
						}),
						(this.setupPeer = function (e, n) {
							if (!e.ID()) throw new Error("The peer id is not defined");
							var r, i, o;
							t.peerList.set(e.ID(), e),
								t.peerAdditionalInfo.set(e.ID(), n),
								t.eventSubject.next(
									new ot.manager.Message({
										Type: 1025,
										ArgumentsEvent: {
											EventName: Jn.SWARM,
											Action: Qn.SIZEUPDATE,
											ArgumentsSwarmSizeUpdate: { Size: t.peerList.size },
										},
									})
								);
							var s = setTimeout(function () {
									"connected" !== e.getState() &&
										(t.managerConnector.next(
											new ot.manager.Message({
												Type: ot.manager.MessageType.MessageTypeSwipeLeft,
												ArgumentsSwipeLeft: { Peer: e.ID() },
											})
										),
										t.cleanPeerConnector(e, Yn.CONNECTERR));
								}, t.connectionTimeout),
								a = e.notifyStateChanges({
									next: function (n) {
										if (t.peerAdditionalInfo.has(e.ID()))
											switch (
												((t.peerAdditionalInfo.get(e.ID()).PeerState = n), n)
											) {
												case "new":
													break;
												case "connected":
													Object(ht.c)(
														"swarm-manager",
														"peer connected: " + e.ID()
													),
														t.eventSubject.next(
															new ot.manager.Message({
																Type: 1025,
																ArgumentsEvent: {
																	EventName: Jn.SWARM,
																	Action: Qn.SIZEUPDATE,
																	ArgumentsSwarmSizeUpdate: {
																		Size: t.peerList.size,
																		Reason: Yn.CONNECTED,
																	},
																},
															})
														),
														t.clearConnectionTimeoutFor(e.ID()),
														t.eventSubject.next(
															new ot.manager.Message({
																Type: 1025,
																ArgumentsEvent: {
																	EventName: Jn.RTC,
																	Action: Qn.OPEN,
																	PeerID: t.id,
																	RemotePeerID: e.ID(),
																},
															})
														),
														o && o.unsubscribe(),
														(o = e.subscribe({
															next: function (n) {
																if (t.peerAdditionalInfo.has(e.ID())) {
																	if (
																		(n.Type ===
																			Dt.peers.MessageType.MessageTypePing &&
																			e
																				.next(
																					new Dt.peers.Message({
																						Type: Dt.peers.MessageType
																							.MessageTypePong,
																						ArgumentsPingPong: {
																							Seq: n.ArgumentsPingPong.Seq,
																						},
																					})
																				)
																				.subscribe({
																					next: function () {
																						t.peerAdditionalInfo.get(
																							e.ID()
																						).SendSeq[1] += 1;
																					},
																					error: function (e) {},
																				}),
																		n.Type ===
																			Dt.peers.MessageType.MessageTypePong)
																	) {
																		var r = n.ArgumentsPingPong.Seq,
																			i = t.peerAdditionalInfo.get(e.ID());
																		i.PongRecevied = r;
																		var s = Date.now();
																		if (i.PingPongRegi[r]) {
																			var a = i.PingPongRegi[r],
																				u = s - a;
																			i.Measurement.DelayMeasures ||
																				(i.Measurement.DelayMeasures = []),
																				i.Measurement.DelayMeasures.length >=
																					Kn.length &&
																					i.Measurement.DelayMeasures.shift(),
																				i.Measurement.DelayMeasures.push(u),
																				(i.Measurement.AvgDelay =
																					i.Measurement.DelayMeasures.map(
																						function (e, t) {
																							return Kn[t] * e;
																						}
																					).reduce(function (e, t) {
																						return e + t;
																					}) /
																					Kn.reduce(function (e, t) {
																						return e + t;
																					})),
																				t.eventSubject.next(
																					new ot.manager.Message({
																						Type: ot.manager.MessageType
																							.MessageTypeEvent,
																						ArgumentsEvent: {
																							EventName: Jn.PINGPONG,
																							Action: Qn.EXCHANGE,
																							ArgumentsPingPongExchange: {
																								Pid: e.ID(),
																								Seq: r,
																								Start: a,
																								End: s,
																								State: "normal",
																							},
																						},
																					})
																				),
																				delete i.PingPongRegi[r];
																		}
																	}
																	t.peerMessageSubject.next([e.ID(), n]);
																} else o && o.unsubscribe();
															},
															error: function (e) {},
															complete: function () {},
														})),
														r && r.unsubscribe(),
														(r = ce(t.pingPongInterval).subscribe(function (n) {
															t.peerAdditionalInfo.has(e.ID())
																? ((t.peerAdditionalInfo.get(e.ID()).PingSend =
																		n),
																  e
																		.next(
																			new Dt.peers.Message({
																				Type: Dt.peers.MessageType
																					.MessageTypePing,
																				ArgumentsPingPong: { Seq: n },
																			})
																		)
																		.subscribe({
																			next: function () {
																				(t.peerAdditionalInfo.get(
																					e.ID()
																				).SendSeq[0] += 1),
																					(t.peerAdditionalInfo.get(
																						e.ID()
																					).PingPongRegi[n] = Date.now());
																			},
																			error: function (e) {},
																		}))
																: r && r.unsubscribe();
														})),
														i && i.unsubscribe(),
														(i = ce(t.pingPongCheckInterval).subscribe(
															function () {
																if (t.peerAdditionalInfo.has(e.ID())) {
																	var n = t.peerAdditionalInfo.get(e.ID());
																	n.PingSend - n.PongRecevied <
																		t.pingPongMaxAllowedDrift ||
																		t.cleanPeerConnector(e, Yn.PINGPONG);
																} else i && i.unsubscribe();
															}
														)),
														(t.peerAdditionalInfo.get(e.ID()).Subscriptions = [
															r,
															o,
															i,
															a,
														]),
														(t.peerAdditionalInfo.get(
															e.ID()
														).ConnectionTimeout = s);
													break;
												case "disconnected":
												case "failed":
													t.cleanPeerConnector(e, Yn.DISCONNECTED),
														t.eventSubject.next(
															new ot.manager.Message({
																Type: 1025,
																ArgumentsEvent: {
																	EventName: Jn.RTC,
																	Action: Qn.CLOSE,
																	PeerID: t.id,
																	RemotePeerID: e.ID(),
																},
															})
														);
											}
										else
											console.warn(
												"swarm-manager",
												"peer not in peerlist, yet still listening to stateChanges",
												e.ID()
											);
									},
									complete: function () {},
								});
							return (
								(t.peerAdditionalInfo.get(e.ID()).Subscriptions = [r, o, i, a]),
								e
							);
						}),
						(this.clearConnectionTimeoutFor = function (e) {
							t.peerAdditionalInfo.has(e) &&
								t.peerAdditionalInfo.get(e).ConnectionTimeout &&
								(clearTimeout(t.peerAdditionalInfo.get(e).ConnectionTimeout),
								(t.peerAdditionalInfo.get(e).ConnectionTimeout = null));
						}),
						(this.handleIncomingMessage = function (e) {
							switch (e.Type) {
								case ot.manager.MessageType.MessageTypeRegistered:
									if (!e.ArgumentsRegistered || !e.ArgumentsRegistered.ID) {
										console.error(
											"swarm-manager",
											"Critical error: msg Registered not correct"
										);
										break;
									}
									(t.id = e.ArgumentsRegistered.ID),
										t.managerConnector.setID(t.id),
										t.eventSubject.next(
											new ot.manager.Message({
												Type: 1025,
												ArgumentsEvent: {
													EventName: Jn.PEER,
													Action: Qn.REGISTERED,
													ArgumentsRegistered: e.ArgumentsRegistered,
												},
											})
										);
									break;
								case ot.manager.MessageType.MessageTypeHereAreSomePeers:
									var n = t.getSwarmSize();
									G(e.ArgumentsHereAreSomePeers.Peers)
										.pipe(
											Gt(function (e) {
												return t.managerConnector.getID() != e;
											}),
											Gt(function (e) {
												return !t.peerList.has(e);
											}),
											un(t.maxSwarmSize * t.offerMaxPercentage - n.Offer)
										)
										.subscribe({
											next: function (e) {
												var n = t.setupPeer(
													t.peerConnectorUtil.createPeerConnector(e),
													{
														PeerType: "a",
														PingSend: 0,
														InitTimestamp: Date.now(),
														SendSeq: [0, 0, 0, 0, 0],
														SendTime: [0, 0, 0, 0, 0],
														PongRecevied: 0,
														Subscriptions: null,
														ConnectionTimeout: null,
														PingPongRegi: [],
														Measurement: { AnnouceCnt: 0, RequestCnt: 0 },
													}
												);
												t.eventSubject.next(
													new ot.manager.Message({
														Type: 1025,
														ArgumentsEvent: {
															EventName: Jn.RTC,
															Action: Qn.INIT,
															PeerID: t.id,
															RemotePeerID: e,
														},
													})
												),
													n.sendOffer().subscribe({
														next: function (n) {
															0 === n[1].length &&
																console.warn(
																	"swarm-manager",
																	"nothing to offer, offer[1].length===0"
																);
															var r = new ot.manager.Message({
																Type: ot.manager.MessageType
																	.MessageTypeSwipeRight,
																ArgumentsSwipeRight: {
																	Peer: e,
																	Offer: n[0],
																	Candidates: n[1],
																},
															});
															t.managerConnector.next(r);
														},
														error: function (e) {},
														complete: function () {},
													});
											},
											complete: function () {},
										});
									break;
								case ot.manager.MessageType.MessageTypePairingRequest:
									if (
										e.ArgumentsPairingRequest.Type ===
										ot.manager.PairingRequestType.PairingRequestType_answer
									) {
										if (t.peerList.has(e.ArgumentsPairingRequest.Peer)) {
											var r = e.ArgumentsPairingRequest.Offer,
												i = e.ArgumentsPairingRequest.Candidates;
											t.peerList
												.get(e.ArgumentsPairingRequest.Peer)
												.receiveAnswer(r, i)
												.subscribe({
													next: function () {},
													complete: function () {},
													error: function (e) {},
												});
										}
									} else if (
										e.ArgumentsPairingRequest.Type ===
										ot.manager.PairingRequestType.PairingRequestType_offer
									) {
										t.getSwarmSize();
										var o = e.ArgumentsPairingRequest.Peer;
										if (t.hasPeer(o)) break;
										if (t.isAnswerSwarmFull()) break;
										t.setupPeer(t.peerConnectorUtil.createPeerConnector(o), {
											PeerType: "b",
											PingSend: 0,
											PongRecevied: 0,
											InitTimestamp: Date.now(),
											SendSeq: [0, 0, 0, 0, 0],
											SendTime: [0, 0, 0, 0, 0],
											Subscriptions: null,
											ConnectionTimeout: null,
											PingPongRegi: [],
											Measurement: { AnnouceCnt: 0, RequestCnt: 0 },
										})
											.sendAnswer(
												e.ArgumentsPairingRequest.Offer,
												e.ArgumentsPairingRequest.Candidates
											)
											.subscribe({
												next: function (e) {
													var n = new ot.manager.Message({
														Type: ot.manager.MessageType.MessageTypeItsAMatch,
														ArgumentsItsAMatch: {
															Peer: o,
															Offer: e[0],
															Candidates: e[1],
														},
													});
													t.managerConnector.next(n);
												},
												error: function (e) {},
												complete: function () {},
											});
									}
							}
						}),
						(this.peerMessageSubject = new E()),
						(this.peerList = new Map()),
						(this.peerAdditionalInfo = new Map()),
						(this.peerConnectorUtil = e || Xn),
						(this.eventSubject = new E()),
						this.eventSubject.subscribe();
				}
				return (
					(e.prototype.setSleep = function (e) {
						return new Promise(function (t) {
							return setTimeout(t, e);
						});
					}),
					(e.prototype.setCurrentTimeVOD = function (e) {
						this.currentTimeVOD = e;
					}),
					(e.prototype.addResourceActions = function (e, t) {
						this.peerAdditionalInfo.has(e) &&
							("annouce" === t &&
								(this.peerAdditionalInfo.get(e).Measurement.AnnouceCnt += 1),
							"request" === t &&
								(this.peerAdditionalInfo.get(e).Measurement.RequestCnt += 1));
					}),
					(e.prototype.getPeerScore = function (e, t) {
						if (!this.peerAdditionalInfo.has(e)) return -1;
						var n = this.peerAdditionalInfo.get(e),
							r = this.peerList.get(e);
						switch (t) {
							case "delay":
								return -n.Measurement.AvgDelay || 0;
							case "favor-age":
								return r.getAge();
							case "favor-low-annouce":
								return -n.Measurement.AnnouceCnt;
						}
						return -1;
					}),
					(e.new = function () {
						return new e();
					}),
					e
				);
			})();
			window.conflib = window.conflib || { log: {} };
			var Zn = "v" + ae.a,
				er = function (e) {
					var t = this;
					(this.started = !1),
						(this.startupTimeSet = !1),
						(this.playerPauseSet = !1),
						(this.registerStr = ""),
						(this.initialBufferStall = !1),
						(this.getResourceManager = function () {
							return t.rm;
						}),
						(this.resetPeerConnectorUtils = function (e) {
							t.sm.setPeerConnectorUtils(e);
						}),
						(this.getSwarmManager = function () {
							return t.sm;
						}),
						(this.register = function (e, n, r, i) {
							return void 0 === i && (i = !1), t.sm.register(e, n, r, i);
						}),
						(this.registerStatsInputPlugin = function (e) {
							return t.sc.register(e), t;
						}),
						(this.registerStatsOutputPlugin = function (e, n) {
							return t.sc.registerOutput(e, n), t;
						}),
						(this.getResource = function (e, n, r) {
							return void 0 === n && (n = 1e4), t.rm.getResource(e, n, r);
						}),
						(this.createEBXHR = function () {
							return new dt().bindResourceManager(t.rm);
						}),
						(this.setTimeoutV2V = function (e) {
							return t.rm.setTimeoutV2V(e), t;
						}),
						(this.start = function () {
							t.started
								? console.warn("Shouldn't have start the lib twice")
								: "Firefox" !== it.name &&
								  (t.sm.start(2e4),
								  t
										.registerStatsInputPlugin(t.sm)
										.registerStatsInputPlugin(t.rm),
								  (t.started = !0));
						}),
						(this.updatePlayerStats = function () {
							if ("Firefox" !== it.name) return t.scout.statsReporter;
						}),
						(this.emitPlayerEvents = function (e) {
							return t.scout.statsReporter.incrementPlayerEvents(e);
						}),
						(this.close = function () {
							(t.started = !1),
								t.psin && t.psin.stop(),
								t.mc.close(),
								t.sm.close(),
								t.sc.close(),
								t.playerEventSubscription &&
									t.playerEventSubscription.unsubscribe(),
								(t.mc = null),
								(t.sm = null),
								(t.sc = null),
								(t.playerEventSubscription = null),
								t.scout && t.scout.stop();
						}),
						(this.setStartupTime = function (e) {
							(t.startupTimeSet = !0),
								"Firefox" !== it.name && t.psin.setStartTime(e);
						}),
						(this.integrate = function (e, n, r) {
							var i,
								o,
								s,
								a,
								u,
								c = Date.now();
							if ((console.info("adapter type : ", n), "Firefox" !== it.name)) {
								if (!r)
									throw (
										(console.error(
											"Cannot integrate to a player without the options"
										),
										Error("Cannot integratie to a player without the options"))
									);
								Array.isArray(e) && "dash" === n && (e = e[0]),
									(t.psin = new at()),
									t.registerStatsInputPlugin(t.psin.start()),
									t.psin.reset(),
									t.psin.setOrigin(r.playerInput.origin),
									t.psin.setContent(r.playerInput.content),
									t.psin.setProtocol(r.playerInput.proto),
									r.playerInput.browserOverride &&
										t.psin.setMobileBrowser(r.playerInput.browserOverride),
									r.playerInput.osOverride &&
										t.psin.setMobileOS(r.playerInput.osOverride),
									r.statsOutput.enable &&
										((t.srout = new gt(
											r.statsOutput.url,
											r.statsOutput.intervalMs
										)),
										t.registerStatsOutputPlugin(
											t.srout.start(),
											"stats-receiver"
										));
								var l = t.managerUrl.split("/").slice(-1)[0];
								(t.scout = new ft(
									(null === (i = r.statsCollectorOutput) || void 0 === i
										? void 0
										: i.serverUrl) || "https://api.easybroadcast.fr/v1",
									r.playerInput.contentUrl
										? r.playerInput.contentUrl
										: r.playerInput.content,
									r.playerInput.proto,
									!1,
									l,
									r.playerInput.content,
									ae.a,
									null === (o = r.statsCollectorOutput) || void 0 === o
										? void 0
										: o.originOverwrite,
									null === (s = r.statsCollectorOutput) || void 0 === s
										? void 0
										: s.userId,
									null === (a = r.statsCollectorOutput) || void 0 === a
										? void 0
										: a.userAgentOverwrite
								)),
									(t.scout.p2pStatsStore = t.p2pStatsStore),
									t.registerStatsOutputPlugin(t.scout, "statscollector"),
									t.scout.start(r.statsOutput.intervalMs || 3e4),
									r.resourceManager.tokenRemover &&
										(t.rm.removeToken = r.resourceManager.tokenRemover),
									t.sm.setPingPongInterval(
										r.swarmManager.pingPongInterval || 5e3
									),
									r.swarmManager.maxSwarmSize &&
										t.sm.setMaxSwarmSize(r.swarmManager.maxSwarmSize),
									t.rm
										.setTimeoutV2V(r.resourceManager.timeoutV2V)
										.setStorageSize(r.resourceManager.storageSize)
										.setRandomWaitForPeers(r.resourceManager.randomWaitForPeers)
										.setAllowByteRequest(r.resourceManager.partialRequest)
										.setEnableV2V(
											null === (u = r.resourceManager.enableV2V) ||
												void 0 === u ||
												u
										);
								var f,
									p,
									h,
									g,
									d,
									y = ((f = n), Be.has(f) ? Be.get(f) : null);
								y.adaptPlayer(e, t),
									(t.playerEventSubscription = y
										.exportEvent(e)
										.pipe(
											((p = function (e) {
												return e.Type;
											}),
											function (e) {
												return e.lift(new L(p, h, g, d));
											}),
											K(function (e) {
												return "register" === e.key
													? e.pipe(
															((t = 100),
															void 0 === n && (n = ne),
															void 0 === r && (r = re),
															function (e) {
																return e.lift(
																	new ie(t, n, r.leading, r.trailing)
																);
															})
													  )
													: e;
												var t, n, r;
											})
										)
										.subscribe(function (n) {
											switch (n.Type) {
												case "canplay":
													var i = (Date.now() - c) / 1e3;
													t.startupTimeSet ||
														((t.startupTimeSet = !0), t.psin.setStartTime(i));
													break;
												case "playing":
													t.psin.setState(ot.manager.PlayingState.PLAYING),
														!0 === t.playerPauseSet &&
															(new Date().getTime() - t.playerPauseTime) /
																1e3 >=
																120 &&
															(console.log("120 seconds crossed, player reset"),
															t.rm.clearStorage(),
															(e[0].currentLevel = e[0].autoLevelEnabled
																? -1
																: e[0].currentLevel),
															(t.playerPauseSet = !1));
													break;
												case "paused":
													t.psin.setState(ot.manager.PlayingState.PAUSED),
														!1 === t.playerPauseSet &&
															((t.playerPauseSet = !0),
															(t.playerPauseTime = new Date().getTime()));
													break;
												case "bufferstalled":
													if (!t.initialBufferStall) {
														t.initialBufferStall = !0;
														break;
													}
													t.p2pStatsStore.addRebuffering(),
														t.psin.setState(ot.manager.PlayingState.BUFFERING),
														t.psin.incRebuffer();
													break;
												case "register":
													n.URL || (n.URL = r.swarmManager.url);
													var o = n.Quality + "-" + n.Codec + "-" + n.URL,
														s = o !== t.registerStr;
													t.register(n.Quality, n.Codec, n.URL, s),
														(t.registerStr = o);
													break;
												case "currentTime":
													t.sm.setCurrentTimeVOD(n.CurrentTime);
													break;
												case "seeking":
													break;
												case "bufferlength":
													t.p2pStatsStore.addBufferLength(n.BufferLength),
														t.psin.setBufferLength(n.BufferLength);
													break;
												case "error":
												case "qualitychangerequested":
													break;
												case "qualitychangerendered":
													t.p2pStatsStore.setQuality(n.Quality),
														t.psin.setBandwidth(n.Quality);
											}
										}));
							} else t.close();
						}),
						console.info(
							"Easybroadcast Technology " + Zn + ". All rights reserved."
						),
						(this.managerUrl = e),
						(this.mc = xt.session().assign(e).start()),
						(this.sm = $n.new().bind(this.mc)),
						(this.rm = new In().bindSwarmManager(this.sm)),
						(this.sc = new kn()),
						(this.p2pStatsStore = new rt(this.sm)),
						(this.mc.p2pStatsStore = this.p2pStatsStore),
						(this.rm.p2pStatsStore = this.p2pStatsStore);
				};
		},
	]);
});
