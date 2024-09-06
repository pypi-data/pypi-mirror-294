/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace sdy {
class ShardableDataFlowOpInterface;
namespace detail {
struct ShardableDataFlowOpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    mlir::ArrayRef<mlir::sdy::TensorShardingAttr> (*getBlockArgumentEdgeOwnerShardings)(const Concept *impl, ::mlir::Operation *);
    void (*setBlockArgumentEdgeOwnerSharding)(const Concept *impl, ::mlir::Operation *, unsigned, mlir::sdy::TensorShardingAttr);
    void (*setBlockArgumentEdgeOwnerShardings)(const Concept *impl, ::mlir::Operation *, mlir::ArrayRef<mlir::sdy::TensorShardingAttr>);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::sdy::ShardableDataFlowOpInterface;
    Model() : Concept{getBlockArgumentEdgeOwnerShardings, setBlockArgumentEdgeOwnerSharding, setBlockArgumentEdgeOwnerShardings} {}

    static inline mlir::ArrayRef<mlir::sdy::TensorShardingAttr> getBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setBlockArgumentEdgeOwnerSharding(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, unsigned index, mlir::sdy::TensorShardingAttr sharding);
    static inline void setBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, mlir::ArrayRef<mlir::sdy::TensorShardingAttr> shardings);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::sdy::ShardableDataFlowOpInterface;
    FallbackModel() : Concept{getBlockArgumentEdgeOwnerShardings, setBlockArgumentEdgeOwnerSharding, setBlockArgumentEdgeOwnerShardings} {}

    static inline mlir::ArrayRef<mlir::sdy::TensorShardingAttr> getBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline void setBlockArgumentEdgeOwnerSharding(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, unsigned index, mlir::sdy::TensorShardingAttr sharding);
    static inline void setBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, mlir::ArrayRef<mlir::sdy::TensorShardingAttr> shardings);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};
template <typename ConcreteOp>
struct ShardableDataFlowOpInterfaceTrait;

} // namespace detail
class ShardableDataFlowOpInterface : public ::mlir::OpInterface<ShardableDataFlowOpInterface, detail::ShardableDataFlowOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<ShardableDataFlowOpInterface, detail::ShardableDataFlowOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::ShardableDataFlowOpInterfaceTrait<ConcreteOp> {};
  /// Returns the shardings of all block argument data flow edge owners.
  mlir::ArrayRef<mlir::sdy::TensorShardingAttr> getBlockArgumentEdgeOwnerShardings();
  /// Sets the shardings of the block argument edge owner with the given index.
  void setBlockArgumentEdgeOwnerSharding(unsigned index, mlir::sdy::TensorShardingAttr sharding);
  /// Sets shardings of all block argument edge owners.
  void setBlockArgumentEdgeOwnerShardings(mlir::ArrayRef<mlir::sdy::TensorShardingAttr> shardings);

    // Gets the sharding of the block argument edge owner with the given index.
    mlir::sdy::TensorShardingAttr getBlockArgumentEdgeOwnerSharding(unsigned index){
      mlir::ArrayRef<mlir::sdy::TensorShardingAttr> argSharding = getBlockArgumentEdgeOwnerShardings();
      if(!argSharding.empty()) {
        return argSharding[index];
      }
      return nullptr;
    }
};
namespace detail {
  template <typename ConcreteOp>
  struct ShardableDataFlowOpInterfaceTrait : public ::mlir::OpInterface<ShardableDataFlowOpInterface, detail::ShardableDataFlowOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace sdy
} // namespace mlir
namespace mlir {
namespace sdy {
template<typename ConcreteOp>
mlir::ArrayRef<mlir::sdy::TensorShardingAttr> detail::ShardableDataFlowOpInterfaceInterfaceTraits::Model<ConcreteOp>::getBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getBlockArgumentEdgeOwnerShardings();
}
template<typename ConcreteOp>
void detail::ShardableDataFlowOpInterfaceInterfaceTraits::Model<ConcreteOp>::setBlockArgumentEdgeOwnerSharding(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, unsigned index, mlir::sdy::TensorShardingAttr sharding) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setBlockArgumentEdgeOwnerSharding(index, sharding);
}
template<typename ConcreteOp>
void detail::ShardableDataFlowOpInterfaceInterfaceTraits::Model<ConcreteOp>::setBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, mlir::ArrayRef<mlir::sdy::TensorShardingAttr> shardings) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).setBlockArgumentEdgeOwnerShardings(shardings);
}
template<typename ConcreteOp>
mlir::ArrayRef<mlir::sdy::TensorShardingAttr> detail::ShardableDataFlowOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getBlockArgumentEdgeOwnerShardings(tablegen_opaque_val);
}
template<typename ConcreteOp>
void detail::ShardableDataFlowOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setBlockArgumentEdgeOwnerSharding(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, unsigned index, mlir::sdy::TensorShardingAttr sharding) {
  return static_cast<const ConcreteOp *>(impl)->setBlockArgumentEdgeOwnerSharding(tablegen_opaque_val, index, sharding);
}
template<typename ConcreteOp>
void detail::ShardableDataFlowOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::setBlockArgumentEdgeOwnerShardings(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, mlir::ArrayRef<mlir::sdy::TensorShardingAttr> shardings) {
  return static_cast<const ConcreteOp *>(impl)->setBlockArgumentEdgeOwnerShardings(tablegen_opaque_val, shardings);
}
} // namespace sdy
} // namespace mlir
